.. _branches:

브랜치를 사용한 작업
====================

.. note:: 알렘빅 0.7.0은 완전히 새로운 버전 관리 모델을 갖는다. 이 모델은
   브랜치 포인트, 머지 포인트, 여러 베이스에서 나온 독립 브랜치를 포함하는
   오래 지속되고 라벨이 붙은 브랜치를 완전히 지원한다. 새로운 버전 관리 모델은
   기존 알렘빅 워크 플로우에 영향을 주지 않는데 중점을 두었다. 모든 명령은
   대부분 기존 명령과 동일하게 작동하며 마이그레이션 파일 형도 변경하지
   않아도 된다. (변경을 권장하는 부분은 있다.) ``alembic_version`` 테이블의
   구조는 전혀 바뀌지 않았다. 그러나 대부분의 알렘빅 명령이 알렘빅 환경을
   "브랜치 모드"로 돌리는 새로운 기능을 제공하기 때문에 더 복잡해진 부분도
   있다. "브랜치 모드"에서 작업하는 것은 "베타" 기능으로 생각하고 여러 새로운
   패러다임과 사용 사례들이 테스트되어야 한다. 가볍게 시도해보길 바란다.

.. versionadded:: 0.7.0

브랜치(branch)란 두개 이상의 버전이 같은 부모 마이그레이션을 참조하는 경우에
마이그레이션 스트림의 한 지점을 말한다. 독립적으로 생성된 알렘빅 리비전 파일을
갖는 두개의 분리된 소스 트리가 하나로 합쳐질 때 브랜치는 자연스럽게 생성된다.
이 때 브랜치들을 하나의 변경 사항 시리즈로 합쳐 각 소스 트리로부터 개별적으로
생성된 데이터베이스가 이후에 합쳐진 결과를 동일하게 참조하도록 하는 것은 어려운
일이다. 브랜치가 나타나는 다른 상황은 브랜치를 직접 생성하는 경우다. 마이그레이션
스트림 상에 어떤 지점에서 여러 마이그레이션 시리즈를 독립적으로 관리하길 원하거나
(예시: 트리 생성) 루트에서 시작하지만 서로 다른 기능을 위해 마이그레이션 스트림을
분리하길 원하는 경우(예시: 포레스트)가 이에 해당한다. 이제 이러한 상황들을 모두
다룰 것이다. 가장 일반적인 경우인 소스-머지에서 시작된 브랜치를 합치는 것부터 시작한다.

:ref:`create_migration`에서 다룬 "어카운트 테이블"에서 시작한다. 가장 베이스가
되는 ``1975ea83b712`` 버전에서 두번째 버전인 ``ae1027a6acf``로 나아간다고 가정하자.
이 두 리비전을 위한 마이그레이션 파일은 우리의 소스 레포지토리에 있다고 하자.
이 때 ``shopping_cart``\ 라는 테이블을 위한 리비전을 포함하는 다른 코드 브랜치를
소스 레포지토리로 머지했다고 생각해보자. 이 리비전은 ``account`` 테이블을 생성했던
첫번째 알렘빅 리비전 다음에 생성되었다. 두번째 소스 트리를 가져오면 새 파일
``27c6a30d7c24_add_shopping_cart_table.py``\ 가 우리의 ``versions`` 디렉토리에 존재한다.
이 파일과 ``ae1027a6acf_add_a_column.py`` 파일 모두 ``1975ea83b712_add_account_table.py`\ 를
"다운그레이드" 리비전으로 참조한다. 설명하자면 다음과 같다. ::

    # main source tree:
    1975ea83b712 (create account table) -> ae1027a6acf (add a column)

    # branched source tree
    1975ea83b712 (create account table) -> 27c6a30d7c24 (add shopping cart table)

위에서 ``1975ea83b712`` 리비전이 **브랜치 포인트**가 된다. 두개의 개별 버전이 같은 부모를 참조한다.
알렘빅 명령 ``branches``\ 로 이를 확인할 수 있다. ::

  $ alembic branches --verbose
  Rev: 1975ea83b712 (branchpoint)
  Parent: <base>
  Branches into: 27c6a30d7c24, ae1027a6acf
  Path: foo/versions/1975ea83b712_add_account_table.py

      create account table

      Revision ID: 1975ea83b712
      Revises:
      Create Date: 2014-11-20 13:02:46.257104

               -> 27c6a30d7c24 (head), add shopping cart table
               -> ae1027a6acf (head), add a column

히스토리에서도 같은 내용을 볼 수 있다. 두개의 ``head`` 엔트리와 ``branchpoint``\ 가 나타난다. ::

    $ alembic history
    1975ea83b712 -> 27c6a30d7c24 (head), add shopping cart table
    1975ea83b712 -> ae1027a6acf (head), add a column
    <base> -> 1975ea83b712 (branchpoint), create account table

``alembic heads`` 명령으로 현재 헤드들을 볼 수 있다. ::

    $ alembic heads --verbose
    Rev: 27c6a30d7c24 (head)
    Parent: 1975ea83b712
    Path: foo/versions/27c6a30d7c24_add_shopping_cart_table.py

        add shopping cart table

        Revision ID: 27c6a30d7c24
        Revises: 1975ea83b712
        Create Date: 2014-11-20 13:03:11.436407

    Rev: ae1027a6acf (head)
    Parent: 1975ea83b712
    Path: foo/versions/ae1027a6acf_add_a_column.py

        add a column

        Revision ID: ae1027a6acf
        Revises: 1975ea83b712
        Create Date: 2014-11-20 13:02:54.849677

일반적인 엔드 타겟 ``head``\ 로 ``upgrade`` 명령을 실행하면 알렘빅은 이제 불분명한 명령으로 인식하지 않는다.
여러개의 ``head``\ 가 있기 때문에 ``upgrade``\ 는 추가 정보를 요구한다. ::

    $ alembic upgrade head
      FAILED: Multiple head revisions are present for given argument 'head'; please specify a specific
      target revision, '<branchname>@head' to narrow to a specific head, or 'heads' for all heads

``upgrade`` 명령은 업그레이드를 수행할 때 아주 적은 옵션을 제공한다. 모든 헤드를 한번에 업그레이드할 지
아니면 특정 헤드로 업그레이드할 지에 대한 정보를 ``upgrade`` 명령에 줄 수 있다. 그러나 두개의 소스 트리가
합쳐지는 경우에는 일반적으로 두개의 브랜치를 합치길 원한다.

브랜치 머지하기
---------------

알렘빅 머지는 두개 이상의 "헤드" 파일을 하나로 합치는 마이그레이션 파일이다.
현재 가지고 있는 두개의 브랜치가 "트리" 구조를  갖고 있다고 해보자.
이 때 머지 파일은 "다이아몬드" 구조를 갖게 된다. ::

                                -- ae1027a6acf -->
                               /                   \
    <base> --> 1975ea83b712 -->                      --> mergepoint
                               \                   /
                                -- 27c6a30d7c24 -->

``alembic merge``\ 를 사용해 머지 파일을 만든다. 이 명령에 ``heads`` 인수를 보내면
모든 헤드를 머지하게 된다. 다음과 같이 개별 리비전 번호를 이어서 보내도 된다. ::

    $ alembic merge -m "merge ae1 and 27c" ae1027 27c6a
      Generating /path/to/foo/versions/53fffde5ad5_merge_ae1_and_27c.py ... done

생성된 머지 파일을 살펴보면 일반적인 마이그레이션 파일과 유사하다.
다른 점은 ``down_revision``\ 이 두개의 리비전을 갖는다는 것이다. ::

    """merge ae1 and 27c

    Revision ID: 53fffde5ad5
    Revises: ae1027a6acf, 27c6a30d7c24
    Create Date: 2014-11-20 13:31:50.811663

    """

    # revision identifiers, used by Alembic.
    revision = '53fffde5ad5'
    down_revision = ('ae1027a6acf', '27c6a30d7c24')
    branch_labels = None

    from alembic import op
    import sqlalchemy as sa


    def upgrade():
        pass


    def downgrade():
        pass

이 파일은 일반적인 마이그레이션 파일이다. 원한다면 다른 마이그레이션 파일들처럼
``upgrade()``, ``downgrade()`` 함수에 :class:`.Operations` 명령을 둘 수도 있다.
여기서 다루는 내용은 합쳐질 두개의 브랜치 간에 있을 모든 조정을 할 수 있는
사용자에게만 사용하도록 제한하는 것이 가장 좋다.

이제 ``heads`` 명령은 ``versions/`` 디렉토리에 있으며 새 헤드로 합쳐진 여러개의 헤드를 말한다. ::

    $ alembic heads --verbose
    Rev: 53fffde5ad5 (head) (mergepoint)
    Merges: ae1027a6acf, 27c6a30d7c24
    Path: foo/versions/53fffde5ad5_merge_ae1_and_27c.py

        merge ae1 and 27c

        Revision ID: 53fffde5ad5
        Revises: ae1027a6acf, 27c6a30d7c24
        Create Date: 2014-11-20 13:31:50.811663

히스토리도 비슷한 결과를 보여준다. 머지 포인트가 새 헤드가 된다. ::

    $ alembic history
    ae1027a6acf, 27c6a30d7c24 -> 53fffde5ad5 (head) (mergepoint), merge ae1 and 27c
    1975ea83b712 -> ae1027a6acf, add a column
    1975ea83b712 -> 27c6a30d7c24, add shopping cart table
    <base> -> 1975ea83b712 (branchpoint), create account table

단일 ``head`` 타겟으로 일반 ``upgrade`` 명령을 진행할 수 있다. ::

    $ alembic upgrade head
    INFO  [alembic.migration] Context impl PostgresqlImpl.
    INFO  [alembic.migration] Will assume transactional DDL.
    INFO  [alembic.migration] Running upgrade  -> 1975ea83b712, create account table
    INFO  [alembic.migration] Running upgrade 1975ea83b712 -> 27c6a30d7c24, add shopping cart table
    INFO  [alembic.migration] Running upgrade 1975ea83b712 -> ae1027a6acf, add a column
    INFO  [alembic.migration] Running upgrade ae1027a6acf, 27c6a30d7c24 -> 53fffde5ad5, merge ae1 and 27c


.. topic:: merge mechanics

  업그레이드 과정은 **위상 정렬** 알고리즘을 사용해 모든 마이그레이션 파일을 트래버스 측량한다.
  마이그레이션 파일 리스트를 링크된 리스트가 아닌 **방향성 비사이클 그래프로**로 취급한다. 트래버스
  측량의 시작점은 데이터베이스의 **현재 헤드**이고 종료 지점은 "헤드" 리비전이나 지정된 리비전이다.

  마이그레이션이 여러개의 헤드가 있는 지점을 지날 때 그 지점의 ``alembic_version`` 테이블은
  각 헤드에 해당하는 여러개의 행을 가지고 있다. 위의 마이그레이션 과정은 각 행의
  ``alembic_version``\ 에 대한 SQL을 출력한다.

    .. sourcecode:: sql

      -- Running upgrade  -> 1975ea83b712, create account table
      INSERT INTO alembic_version (version_num) VALUES ('1975ea83b712')

      -- Running upgrade 1975ea83b712 -> 27c6a30d7c24, add shopping cart table
      UPDATE alembic_version SET version_num='27c6a30d7c24' WHERE alembic_version.version_num = '1975ea83b712'

      -- Running upgrade 1975ea83b712 -> ae1027a6acf, add a column
      INSERT INTO alembic_version (version_num) VALUES ('ae1027a6acf')

      -- Running upgrade ae1027a6acf, 27c6a30d7c24 -> 53fffde5ad5, merge ae1 and 27c
      DELETE FROM alembic_version WHERE alembic_version.version_num = 'ae1027a6acf'
      UPDATE alembic_version SET version_num='53fffde5ad5' WHERE alembic_version.version_num = '27c6a30d7c24'

  데이터베이스의 ``27c6a30d7c24``, ``ae1027a6acf`` 리비전이 모두 존재하는 지점에서
  두 값은 모두 두개의 행을 갖는 ``alembic_version`` 테이블에 있다. 이 두 버전으로
  업그레이드 하고 ``alembic current``\ 를 실행하면 다음과 같이 나타난다. ::

      $ alembic current --verbose
      Current revision(s) for postgresql://scott:XXXXX@localhost/test:
      Rev: ae1027a6acf
      Parent: 1975ea83b712
      Path: foo/versions/ae1027a6acf_add_a_column.py

          add a column

          Revision ID: ae1027a6acf
          Revises: 1975ea83b712
          Create Date: 2014-11-20 13:02:54.849677

      Rev: 27c6a30d7c24
      Parent: 1975ea83b712
      Path: foo/versions/27c6a30d7c24_add_shopping_cart_table.py

          add shopping cart table

          Revision ID: 27c6a30d7c24
          Revises: 1975ea83b712
          Create Date: 2014-11-20 13:03:11.436407

  ``merge`` 프로세스의 핵심적인 장점은 ``ae1027a6acf`` 버전만 존재하는 데이터베이스나
  ``27c6a30d7c24`` 버전만 존재하는 데이터베이스에서 동일하게 실행된다는 것이다.
  이전에 어떤 버전이 적용되었는지와 관계없이 머지 포인트로 합쳐지기 전에 적용된다.
  리비전 파일 뿐 아니라 머지 파일에 대해서도 생각해볼 필요가 있다. 위상 정렬의 속한
  집합에서 "노드"로 취급되므로 각 노드는 모든 의존 요소가 만족될 때까지 만날 수 없다.

  알렘빅이 머지 포인트를 지원하기 전에는 다른 헤드에 위치한 데이터베이스는 조화롭게
  사용하는 것은 불가능했다. 하나의 마이그레이션이 다른 마이그레이션 이전에 존재하도록
  수동으로 헤드 파일을 쪼개야하므로 다른 마이그레이션에 존재하는 데이터베이스와 호환되지 않는.

브랜치를 명시해 작업하기
------------------------

여러 헤드를 관리할 때  ``alembic upgrade`` 명령에서 사용할 수 있는 다른 옵션이 있었다.
``ae1027a6acf``\ 와 ``27c6a30d7c24`` 두개의 헤드를 갖는 상황으로 돌아가보자. ::

    $ alembic heads
    27c6a30d7c24
    ae1027a6acf

앞에서 ``alembic upgrade head`` 명령을 사용했을 때는 에러가 발생하고
``please specify a specific target revision, '<branchname>@head' to
narrow to a specific head, or 'heads' for all heads`` 메세지가 나타났다.
이제 이 두가지 옵션에 대해서 다룬다.

모든 헤드를 한번에 참조하기
^^^^^^^^^^^^^^^^^^^^^^^^^^^

``heads`` 식별자는 ``head``\ 와 아주 비슷하다. 하지만 ``heads``\ 는 모든 헤드를 한번에 참조한다.
알렘빅은 이를 ``ae1027a6acf``\ 와 ``27c6a30d7c24``\ 에 동시에 작업을 수행하라는 것으로 인식한다.
새로운 데이터베이스에서 ``upgrade heads``\ 를 실행하면 다음과 같이 나타난다. ::

    $ alembic upgrade heads
    INFO  [alembic.migration] Context impl PostgresqlImpl.
    INFO  [alembic.migration] Will assume transactional DDL.
    INFO  [alembic.migration] Running upgrade  -> 1975ea83b712, create account table
    INFO  [alembic.migration] Running upgrade 1975ea83b712 -> ae1027a6acf, add a column
    INFO  [alembic.migration] Running upgrade 1975ea83b712 -> 27c6a30d7c24, add shopping cart table

``heads``\ 로 업그레이드 했기 때문에 실제로 두개의 헤드가 존재한다.
이는 두개의 구별되는 헤드가 ``alembic_version`` 테이블에 존재한다는 의미다.
``alembic current``\ 를 실행하면 다음과 같이 나타난다. ::

    $ alembic current
    ae1027a6acf (head)
    27c6a30d7c24 (head)

현재 ``alembic_version`` 테이블에 두개의 행이 있다. 이 때 한 스탭 만큼 다운그레이드를 하면
알렘빅은 ``alembic_version`` 테이블에 하나의 브랜치만 남도록 브랜치를 삭제한다.
그 다음에 다운그레이드를 하면 남은 하나의 값을 이전 버전으로 내린다. ::

    $ alembic downgrade -1
    INFO  [alembic.migration] Running downgrade ae1027a6acf -> 1975ea83b712, add a column

    $ alembic current
    27c6a30d7c24 (head)

    $ alembic downgrade -1
    INFO  [alembic.migration] Running downgrade 27c6a30d7c24 -> 1975ea83b712, add shopping cart table

    $ alembic current
    1975ea83b712 (branchpoint)

    $ alembic downgrade -1
    INFO  [alembic.migration] Running downgrade 1975ea83b712 -> , create account table

    $ alembic current

특정 버전 참조하기
^^^^^^^^^^^^^^^^^^

``upgrade``\ 에 특정 버전 번호를 보낼 수 있다. 알렘빅은 이 버전이 의존하는 모든 버전을 불러오고
그 외의 버전은 호출하지 않는다고 보장할 수 있다. 따라서 ``27c6a30d7c24`` 리비전이나 ``ae1027a6acf``
리비전을 명시해서 업그레이드하면 ``1975ea83b712`` 리비전이 적용되며 지정한 리비전과 계층이 같은
다른 버전은 적용되지 않는다는 것을 보장할 수 있다. ::

    $ alembic upgrade 27c6a
    INFO  [alembic.migration] Running upgrade  -> 1975ea83b712, create account table
    INFO  [alembic.migration] Running upgrade 1975ea83b712 -> 27c6a30d7c24, add shopping cart table

``ae1027a6acf`` 리비전은 ``1975ea83b712``\ 과 ``27c6a30d7c24`` 두 리비전이 적용된 추가 단일 리비전이다. ::

    $ alembic upgrade ae102
    INFO  [alembic.migration] Running upgrade 1975ea83b712 -> ae1027a6acf, add a column

브랜치 라벨로 작업하기
^^^^^^^^^^^^^^^^^^^^^^

오래 지속되는 브랜치들을 가진 환경을 사용하는 경우를 위해 알렘빅은 **브랜치 라벨**을 지원한다.
이 개념은 다음 절에서 다룰 독립 브랜치의 경우에 특히 유용하다. 이 라벨은 마이그레이션 파일에
있는 문자열 값으로 ``branch_labels``\ 이라는 새로운 식별자를 사용한다. 예를 들어,
"shopping cart" 브랜치를 "shoppingcart"라는 이름을 사용해 참조할 수 있다. 다음과 같이
``27c6a30d7c24_add_shopping_cart_table.py`` 파일에 이름을 추가한다. ::

    """add shopping cart table

    """

    # revision identifiers, used by Alembic.
    revision = '27c6a30d7c24'
    down_revision = '1975ea83b712'
    branch_labels = ('shoppingcart',)

    # ...

``branch_labels`` 속성은 이름 문자열이나 이름으로 구성된 튜플을 참조한다. 이 이름은 현재
리비전과 모든 하위 리비전에 적용된다. 현재 리비전부터 이전 브랜치 포인트까지의 모든 상위
리비전에도 적용될 수 있다. 이 예시에서 브랜치 포인트는 ``1975ea83b712``\ 가 된다.
``shoppingcart`` 라벨이 현재 리비전에 적용된 것을 볼 수 있다. ::

    $ alembic history
    1975ea83b712 -> 27c6a30d7c24 (shoppingcart) (head), add shopping cart table
    1975ea83b712 -> ae1027a6acf (head), add a column
    <base> -> 1975ea83b712 (branchpoint), create account table

라벨이 적용되면 ``shoppingcart``\ 라는 이름은 ``27c6a30d7c24`` 리비전을 위한 별칭처럼 사용된다.
``alembic show`` 명령으로 이를 확인할 수 있다. ::

    $ alembic show shoppingcart
    Rev: 27c6a30d7c24 (head)
    Parent: 1975ea83b712
    Branch names: shoppingcart
    Path: foo/versions/27c6a30d7c24_add_shopping_cart_table.py

        add shopping cart table

        Revision ID: 27c6a30d7c24
        Revises: 1975ea83b712
        Create Date: 2014-11-20 13:03:11.436407

그러나 브랜치 라벨을 사용할 때는 보통 라벨을 "branch at" 문법에 사용하길 원한다.
이 문법으로 원하는 특정 리비전을 선언할 수 있다. 특정 리비전을 "head" 리비전이라고 하자.
헤드가 여러개 존재할 때 ``alembic upgrade head``\ 를 사용해 참조를 할 수 없다.
이러한 경우에 ``shoppingcart@head`` 문법을 사용하면 특정 헤드를 지정할 수 있다. ::

    $ alembic upgrade shoppingcart@head
    INFO  [alembic.migration] Running upgrade 1975ea83b712 -> 27c6a30d7c24, add shopping cart table

여러개의 기존 브랜치는 계속 관리하면서 버전 디렉토리에 새로운 마이그레이션 파일을 추가해야 할 때
``shoppingcart@head`` 문법이 중요해진다. 헤드가 여러개 있을 때 특정한 부모 리비전 없이 새로운
리비전 파일을 추가하려고 하면 ``upgrade`` 명령의 경우처럼 익숙한 에러가 발생하게 된다. ::

    $ alembic revision -m "add a shopping cart column"
      FAILED: Multiple heads are present; please specify the head revision on
      which the new revision should be based, or perform a merge.

위와 같은 경우에 ``alembic revision`` 명령으로 해야할 일은 명확하다. ``shoppingcart`` 브랜치에 한정해
새 리비전을 추가하려면 ``--head`` 인수를 사용하면 된다. 식별자 ``27c6a30d7c24``\ 를 사용해 버전을 지정해도 되고
브랜치명을 사용한 ``shoppingcart@head`` 문법으로 지정해도 된다. ::

    $ alembic revision -m "add a shopping cart column"  --head shoppingcart@head
      Generating /path/to/foo/versions/d747a8a8879_add_a_shopping_cart_column.py ... done

이제 ``alembic history``\ 를 사용하면 ``shoppingcart`` 브랜치에 속하는 두개의 파일을 볼 수 있다. ::

    $ alembic history
    1975ea83b712 -> ae1027a6acf (head), add a column
    27c6a30d7c24 -> d747a8a8879 (shoppingcart) (head), add a shopping cart column
    1975ea83b712 -> 27c6a30d7c24 (shoppingcart), add shopping cart table
    <base> -> 1975ea83b712 (branchpoint), create account table

다음과 같이 ``shoppingcart`` 브랜치에 대한 히스토리만을 볼 수도 있다. ::

    $ alembic history -r shoppingcart:
    27c6a30d7c24 -> d747a8a8879 (shoppingcart) (head), add a shopping cart column
    1975ea83b712 -> 27c6a30d7c24 (shoppingcart), add shopping cart table

베이스에서 시작해 ``shoppingcart``\ 까지의 모든 경로를 보고 싶다면 다음과 같이 한다. ::

    $ alembic history -r :shoppingcart@head
    27c6a30d7c24 -> d747a8a8879 (shoppingcart) (head), add a shopping cart column
    1975ea83b712 -> 27c6a30d7c24 (shoppingcart), add shopping cart table
    <base> -> 1975ea83b712 (branchpoint), create account table

위 명령의 "head"를 "base"로 바꿔도 된다. 조금 다른 결과가 나타난다. ::

    $ alembic history -r shoppingcart@base:
    1975ea83b712 -> ae1027a6acf (head), add a column
    27c6a30d7c24 -> d747a8a8879 (shoppingcart) (head), add a shopping cart column
    1975ea83b712 -> 27c6a30d7c24 (shoppingcart), add shopping cart table
    <base> -> 1975ea83b712 (branchpoint), create account table

``shoppingcart@base``\ 에서 시작해 엔드포인트 없이 나열하고 싶다면 ``-r shoppingcart@base:heads``\
를 붙이면 모든 헤드가 나열된다. ``shoppingcart@base``\ 가 ``ae1027a6acf`` 리비전과 같은 "base"를
공유하기 때문에 이 리비전도 나열되는 목록에 포함된다. ``<branchname>@base`` 문법은 개별 베이스들을
다룰 때 유용하다. 개별 베이스는 다음 절에서 다룬다.

``<branchname>@head`` 형식에 브랜치명 대신 리비전 번호를 사용할 수도 있지만 편리한 방법은 아니다.
라벨이 없는 ``ae1027a6acf`` 리비전을 포함하는 브랜치에 새 리비전을 추가하고 싶지만 이 리비전이 헤드가
아닌 경우에는 다음과 같은 명령으로 ``ae1027a6acf``\ 를 포함하는 브랜치의 헤드를 찾을 수 있다. ::

    $ alembic revision -m "add another account column" --head ae10@head
      Generating /path/to/foo/versions/55af2cb1c267_add_another_account_column.py ... done

추가 라벨 문법
^^^^^^^^^^^^^^

라벨이 붙은 브랜치가 여러 브랜치로 나눠지는 경우에 ``heads`` 심볼을 브랜치 라벨과 합칠 수도 있다. ::

    $ alembic upgrade shoppingcart@heads

:ref:`relative_migrations`\ 에서 다룬 상대 식별자도 라벨과 사용할 수 있다. 예를 들어,
``shoppingcart@+2``\ 로 업그레이드를 하면 "shoppingcart"의 헤드로부터 2개의 리비전 만큼
업그레이드하게 된다. ::

    $ alembic upgrade shoppingcart@+2

히스토리에도 사용할 수 있다. ::

    $ alembic history -r current:shoppingcart@+2

새로운 ``relnum+delta`` 형식도 사용할 수 있다. 예를 들어, ``shoppingcart``\ 의
헤드로부터 2개의 리비전 이전까지 나열하고 싶다면 다음과 같이 한다. ::

    $ alembic history -r :shoppingcart@head-2

.. _multiple_bases:

여러 베이스로 작업하기
----------------------

.. note::  다중 베이스 기능은 **동일한 alembic_version 테이블**을 공유하는
   알렘빅 버전 관리 계통을 여러개 사용하는 것을 허용하기 위해 고안되었다.
   이를 통해 관리 계통에 있는 개별 리비전들이 서로에게 상호 의존할 수 있다.
   하나의 프로젝트가 다수의 **완전히 독립적인** 리비전 계통들을 가지면서
   이 리비전들이 **개별적인** alembic_version 테이블들을 참조하는 경우에 대한
   간다한 예시는 :ref:`multiple_environments`\ 를 본다.

이전 절에서 다수의 헤드에 ``alembic upgrade``\ 를 사용해도 문제가 없다는 것을
확인했다. ``alembic revision``\ 은 새 리비전 파일과 연관지을 헤드를 지정할 수 있고
브랜치 라벨을 사용하면 명령 옵션에 사용할 수 있는 이름을 브랜치에 지정할 수 있다.
이러한 기능들을 새로운 베이스를 참조하는데 사용해보자. 이 베이스는 우리가 이전에 다룬
account/shopping cart 리비전과 부분 독립적인 완전히 새로운 리비전 파일 트리가 된다.
이 파일 트리는 "networking"과 관련된 테이블을 관리한다.

.. _multiple_version_directories:

여러 버전 디렉토리 설정
^^^^^^^^^^^^^^^^^^^^^^^

선택적이지만 여러 베이스로 작업할 때 서로 다른 버전 파일 모음들이 각각 자신의 디렉토리에
위치하길 원하는 경우가 자주 있다. 일반적으로 어플리케이션이 여러개의 서브 모듈로 구성될 때
각 모듈은 그 모듈과 관계된 마이그레이션들을 모함하는버전 디렉토리를 갖는다. 시작을 위해
``alembic.ini`` 파일이 여러개의 디렉토리를 참조하도록 수정한다. 이 중 하나를 현재
``versions`` 디렉토리로 선언할 것이다. ::

  # version location specification; this defaults
  # to foo/versions.  When using multiple version
  # directories, initial revisions must be specified with --version-path
  version_locations = %(here)s/model/networking %(here)s/alembic/versions

새 디렉토리 ``%(here)s/model/networking``\ 은 ``alembic.ini`` 파일이 있는 디렉토리에 있고
``%(here)s``\ 를 사용해 경로를 확인한다. 이 디렉토리에 처음으로 새 리비전 파일을 생성할 때
``model/networking``\ 가 존재하지 않으면 자동으로 생성된다. 이 곳에 리비전을 한번 생성하고
나면 이 리비전 트리를 참조하는 후속 리비전 파일이 생성될 때 이 경로를 사용한다.

라벨이 있는 베이스 리비전 생성하기
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

새 브랜치가 이름을 지정하길 원하고 이를 위해 베이스에 브랜치 라벨을 적용하고 싶다.
``alembic revision`` 명령을 그대로 사용하면 된다. 이 때 새로운 리비전 파일을 생성하기
위해 사용되는 ``script.py.mako`` 파일에 적절한 대체가 있는다는 것을 보장해야 한다.
기존 마이그레이션 환경을 생성하는데 사용된 알렘빅 버전이 0.7.0 이상이면 이미 보장되어 있다.
만약 0.7.0 이전 버전으로 생성된 환경으로 작업한다면 ``script.py.mako``\ 에 명령을 추가해야
한다. 보통은 아래 예시처럼 ``down_revision`` 명령 아래에 추가한다. ::

    # revision identifiers, used by Alembic.
    revision = ${repr(up_revision)}
    down_revision = ${repr(down_revision)}

    # add this here in order to use revision with branch_label
    branch_labels = ${repr(branch_labels)}

이제 새로운 리비전 파일을 생성할 수 있다. 네트워킹과 관련된 테이블을 관리하는 브랜치로
시작해보자. ``--head`` 버전을 ``base``\ 로 ``--branch-label``\ 을 ``networking``\ 으로 지정하고
첫번째 리비전 파일이 위치할 디렉토리를 ``--version-path`` 옵션에 지정한다. ::

    $ alembic revision -m "create networking branch" --head=base --branch-label=networking --version-path=model/networking
      Creating directory /path/to/foo/model/networking ... done
      Generating /path/to/foo/model/networking/3cac04ae8714_create_networking_branch.py ... done

위 명령을 실행할 때 ``script.py.mako``\ 에 새 명령이 없으면 다음과 같은 에러가 나타난다. ::

  FAILED: Version 3cac04ae8714 specified branch_labels networking, however
  the migration file foo/model/networking/3cac04ae8714_create_networking_branch.py
  does not have them; have you upgraded your script.py.mako to include the 'branch_labels'
  section?

위 에러가 발생한 후에 다시 시도하고 싶다면 이전 명령으로 잘못 생성된 파일을 삭제하거나
``3cac04ae8714_create_networking_branch.py`` 파일을 직접 수정해 우리가 선택한 ``branch_labels``\ 을 추가한다.

여러 베이스로 실행하기
^^^^^^^^^^^^^^^^^^^^^^

영구적인 새 베이스를 시스템에 만들고 나면 항상 여러개의 헤드가 존재하게 된다. ::

    $ alembic heads
    3cac04ae8714 (networking) (head)
    27c6a30d7c24 (shoppingcart) (head)
    ae1027a6acf (head)

새 리비전 파일을 ``networking``\ 에 추가하길 원할 때는 ``networking@head``\ 를 ``--head``\
로 지정한다. 이제 선택한 헤드에 기반해 적절한 버전 디렉토리가 자동으로 선택된다. ::

    $ alembic revision -m "add ip number table" --head=networking@head
      Generating /path/to/foo/model/networking/109ec7d132bf_add_ip_number_table.py ... done

``networking@head``\ 를 사용해 헤드를 참조하는 것이 중요하다. ``networking``\ 만을 참조하면
``3cac04ae8714``\ 만을 참조하게 된다. 이 리비전을 참조했는데 헤드가 아니라면 ``alembic revision``\ 은
다음과 같이 헤드 리비전을 확인한다. ::

    $ alembic revision -m "add DNS table" --head=networking
      FAILED: Revision 3cac04ae8714 is not a head revision; please
      specify --splice to create a new branch from this revision

앞서 다뤘듯이 이 베이스는 독립적이기 때문에 베이스로부터 시작하는 히스토리를
``history -r networking@base:`` 명령으로 볼 수 있다. ::

    $ alembic history -r networking@base:
    109ec7d132bf -> 29f859a13ea (networking) (head), add DNS table
    3cac04ae8714 -> 109ec7d132bf (networking), add ip number table
    <base> -> 3cac04ae8714 (networking), create networking branch

현재 시점에서는 ``-r :networking@head``\ 를 사용한 것과 같은 결과지만
추가 명령어를 사용하고 나면 다른 결과가 나타날 것이다.

이제 개별 브랜치 간에 업그레이드와 다운그레이드를 자유롭게 할수 있다.
(빈 데이터베이스를 가정한다.) ::

    $ alembic upgrade networking@head
    INFO  [alembic.migration] Running upgrade  -> 3cac04ae8714, create networking branch
    INFO  [alembic.migration] Running upgrade 3cac04ae8714 -> 109ec7d132bf, add ip number table
    INFO  [alembic.migration] Running upgrade 109ec7d132bf -> 29f859a13ea, add DNS table

``heads``\ 를 사용해 전부 업그레이드 할 수도 있다. ::

    $ alembic upgrade heads
    INFO  [alembic.migration] Running upgrade  -> 1975ea83b712, create account table
    INFO  [alembic.migration] Running upgrade 1975ea83b712 -> 27c6a30d7c24, add shopping cart table
    INFO  [alembic.migration] Running upgrade 27c6a30d7c24 -> d747a8a8879, add a shopping cart column
    INFO  [alembic.migration] Running upgrade 1975ea83b712 -> ae1027a6acf, add a column
    INFO  [alembic.migration] Running upgrade ae1027a6acf -> 55af2cb1c267, add another account column

브랜치 의존 요소
----------------

여러개의 루트로 작업할 때 여러개의 다른 리비전 스트림이 다른 리비전 스트림을
참조할 수도 있다. 예를 들어, ``account`` 테이블을 참조해야 하는 ``networking``\
의 새 리비전이 ``55af2cb1c267, add another account column`` 리비전을 의존 요소로 설정하길 원한다.
이 리비전은 ``account`` 테이블에 적용된 마지막 리비전이다. 그래프 관점에서 이는
``55af2cb1c267, add another account column``\ 와 ``29f859a13ea, add DNS table``\ 을 모두
다운 리비전으로 하는 새로운 파일에 지나지 않는다. 두 리비전을 머지한 것처럼 보인다.
하지만 ``networking``\ 에 있는 버전이 다른 스트림의 어떤 지점에 도달하더라도
이 두 리비전 스트림이 머지된 것이 아니라 독립적인 것으로 남길 원한다. 이러한 사례를 지원하기 위해
알림빅은 ``depends_on``\ 이라는 명령어를 제공한다. 이 명령을 사용하면 리비전 파일이 다른 리비전을
"의존 요소"로 참조하게 된다. 그래프 관점에서 ``down_revision``\ 과 유사하지만 의미적인 관점에서는 다르다.

``alembic revision`` 명령의 일부로 지정해 ``depends_on``\ 을 사용할 수 있다. ::

    $ alembic revision -m "add ip account table" --head=networking@head  --depends-on=55af2cb1c267
      Generating /path/to/foo/model/networking/2a95102259be_add_ip_account_table.py ... done

마이그레이션 파일에서 새 명령어가 생긴 것을 볼 수 있다. ::

    # revision identifiers, used by Alembic.
    revision = '2a95102259be'
    down_revision = '29f859a13ea'
    branch_labels = None
    depends_on='55af2cb1c267'

``depends_on``\ 은 실제 디비전 번호나 브랜치 이름이 될 수 있다. 명령줄에서 지정할 때
리비전 번호의 일부만 지정하는 것도 지원된다. 참조할 수 있는 의존 리비전 갯수에는 제한이 없다.
예를 들어, 다음과 같은 명령을 사용할 수 있다. ::

    $ alembic revision -m "add ip account table" \\
        --head=networking@head  \\
        --depends-on=55af2cb1c267 --depends-on=d747a --depends-on=fa445
      Generating /path/to/foo/model/networking/2a95102259be_add_ip_account_table.py ... done

파일에는 다음과 같이 나타난다. ::

    # revision identifiers, used by Alembic.
    revision = '2a95102259be'
    down_revision = '29f859a13ea'
    branch_labels = None
    depends_on = ('55af2cb1c267', 'd747a8a8879', 'fa4456a9201')

리비전 파일이 생성된 후에 ``--depends-on`` 인수를 사용하지 않고 수동으로 의존 리비전
값을 추가하거나 수정해도 된다.

.. versionadded:: 0.8 ``depends_on`` 속성은 파일을 직접 수정하지 않고
   ``alembic revision`` 명령으로 바로 지정될 수 있다. ``depends_on``
   식별자는 명령줄에서 브랜치 이름으로 지정되거나 마이그레이션 파일에서
   바로 지정될 수 있다. 명령줄에서 부분 리비전 번호로 지정된 값은 출력
   파일에서는 전체 리비전 번호로 변환된다.

"heads"로부터 ``networking`` 브랜치의 히스토리를 보면 이 명령이 어떤 효과를 갖는지
확인할 수 있다. 예를 들어, 하위에 오는 모든 리비전이 나타난다. ::

    $ alembic history -r :networking@head
    29f859a13ea (55af2cb1c267) -> 2a95102259be (networking) (head), add ip account table
    109ec7d132bf -> 29f859a13ea (networking), add DNS table
    3cac04ae8714 -> 109ec7d132bf (networking), add ip number table
    <base> -> 3cac04ae8714 (networking), create networking branch
    ae1027a6acf -> 55af2cb1c267 (effective head), add another account column
    1975ea83b712 -> ae1027a6acf, Add a column
    <base> -> 1975ea83b712 (branchpoint), create account table

헤드로 업그레이드 하는 방향으로 ``networking`` 브랜치의 전체 히스토리를 볼 수 있다. 이 히스토리에서
``55af2cb1c267, add another account column``\ 로 빌드되는 트리가 먼저 나타난다. 흥미롭게도 이 트리는
``networking@base``\ 와 같이 다른 방향으로의 히스토리를 볼 때는 나타나지 않는다. ::

    $ alembic history -r networking@base:
    29f859a13ea (55af2cb1c267) -> 2a95102259be (networking) (head), add ip account table
    109ec7d132bf -> 29f859a13ea (networking), add DNS table
    3cac04ae8714 -> 109ec7d132bf (networking), add ip number table
    <base> -> 3cac04ae8714 (networking), create networking branch

이러한 차이가 나타나는 이유는 베이스로부터 히스토리를 보여줄 때 업그레이드가 아니고 다운그레이드를
했을 때 나타나는 것을 보여주기 때문이다. 만약 ``networking``\ 에 있는 모든 파일을 ``networking@base``\ 를
사용해 다운그레이드하면 의존 요소들은 영향을 받지 않고 그대로 유지된다.

이 때 ``heads``\ 를 봐도 이상한 점이 나타난다. ::

    $ alembic heads
    2a95102259be (networking) (head)
    27c6a30d7c24 (shoppingcart) (head)
    55af2cb1c267 (effective head)

우리가 "dependency"로 사용했던 파일 ``55af2cb1c267``\ 가 "effective head"로 나타난다.
이러한 헤드는 이전에 본 히스토리에도 나타난 적이 있다. 이는 모든 버전을 최상위로 업그레이드하면
리비전 번호 ``55af2cb1c267``\ 는 실제로 ``alembic_version`` 테이블에는 나타나지 않는다는 의미다.
이 리비전에 의존하는 ``2a95102259be`` 리비전 이후에 오는 브랜치가 없기 때문이다. ::

    $ alembic upgrade heads
    INFO  [alembic.migration] Running upgrade 29f859a13ea, 55af2cb1c267 -> 2a95102259be, add ip account table

    $ alembic current
    2a95102259be (head)
    27c6a30d7c24 (head)

알렘빅도 이 리비전이 진짜 리비전은 아니라는 것은 인식하고 있지만 개발자들은 의미적으로
헤드처럼 인지하고 있기 때문에 ``alembic heads`` 명령을 사용했을 때 엔트리가 나타나게 된다.
``alembic current`` 명령에는 나타나지 않지만 ``alembic heads`` 명령이 "effective head"의
특별한 상태를 알려주기 때문에 혼동하지 않을 수 있다.

``55af2cb1c267``\ 에 새 리비전을 추가하면 브랜치는 다시 데이터베이스에 자신의 엔트리를 갖는 진짜 브랜치가 된다. ::

    $ alembic revision -m "more account changes" --head=55af2cb@head
      Generating /path/to/foo/versions/34e094ad6ef1_more_account_changes.py ... done

    $ alembic upgrade heads
    INFO  [alembic.migration] Running upgrade 55af2cb1c267 -> 34e094ad6ef1, more account changes

    $ alembic current
    2a95102259be (head)
    27c6a30d7c24 (head)
    34e094ad6ef1 (head)


리비전 트리는 이제 다음과 같이 나타난다. ::

    $ alembic history
    29f859a13ea (55af2cb1c267) -> 2a95102259be (networking) (head), add ip account table
    109ec7d132bf -> 29f859a13ea (networking), add DNS table
    3cac04ae8714 -> 109ec7d132bf (networking), add ip number table
    <base> -> 3cac04ae8714 (networking), create networking branch
    1975ea83b712 -> 27c6a30d7c24 (shoppingcart) (head), add shopping cart table
    55af2cb1c267 -> 34e094ad6ef1 (head), more account changes
    ae1027a6acf -> 55af2cb1c267, add another account column
    1975ea83b712 -> ae1027a6acf, Add a column
    <base> -> 1975ea83b712 (branchpoint), create account table


                        --- 27c6 --> d747 --> <head>
                       /   (shoppingcart)
    <base> --> 1975 -->
                       \
                         --- ae10 --> 55af --> <head>
                                        ^
                                        +--------+ (dependency)
                                                 |
                                                 |
    <base> --> 3782 -----> 109e ----> 29f8 ---> 2a95 --> <head>
             (networking)


브랜치, 머지, 라벨링을 남용하면 일이 아주 많이 복잡해질 것이다.
따라서 브랜치 시스템은 최선의 결과를 위해서만 주의깊게 사용해야 한다.
