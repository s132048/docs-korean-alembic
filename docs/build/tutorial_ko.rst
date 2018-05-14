========
튜토리얼
========

`Alembic <http://bitbucket.org/zzzeek/alembic>`_\ 는 관계형 데이터베이스를 위한
*변경 관리*\ 의 생성, 관리, 실행을 제공하며, `SQLAlchemy <http://www.sqlalchemy.org>`_\ 을
기본 엔진으로 사용한다. 이 튜토리얼은 이 도구의 사용과 이론에 대한 전체적으로 소개하고 있다.

시작하기 전에 Alembic이 :ref:`installation`\ 에 설명된대로 설치되었는지 확인하라.

마이그레이션 환경(The Migration Environment)
============================================

Alembic는 *마이그레이션 환경*\ 을 생성하는 것부터 시작한다. 이 환경은 특정한 어플리케이션에
한정된 스크립트의 디렉토리다. 이 마이그레이션 환경은 한 번만 생성되며 그 이후 어플리케이션의
소스코드 자체로 유지된다. 환경은 Alembic의 ``init`` 커맨드를 사용해서 생성되며 어플리케이션의
특정한 요구에 맞춰 커스터마이징할 수도 있다.

환경의 구조는 생성된 마이그레이션 스크립트를 포함하고 있으며 아래와 같다::

    yourproject/
        alembic/
            env.py
            README
            script.py.mako
            versions/
                3512b954651e_add_account.py
                2b1ae634e5cd_add_order_id.py
                3adcc9a56557_rename_username_field.py

디렉토리는 아래의 디렉토리와 파일을 포함한다:

* ``yourproject`` - 이 디렉토리는 어플리케이션의 소스코드의 루트 또는 루트 내에 있는 디렉토리가 될 수 있다.
* ``alembic`` - 이 디렉토리는 어플리케이션의 소스 트리 내부에 위치하며,
  마이그레이션 환경의 홈이 된다. 어느 이름이라도 상관없으며 여러 데이터베이스를 사용하는 프로젝트의 경우
  하나 이상을 가지고 있을 수 있다.
* ``env.py`` - 파이썬 스크립트로 Alembic 마이그레이션 도구가 실행될 때마다 실행된다.
  최소 이 파일은 SQLAlchemy 엔진을 생성하고 설정하기 위한 명령을 포함하고 있으며
  트랜잭션으로 엔진에서 연결을 획득한 후 마이그레이션 엔진을 실행시킨다. 이 때,
  해당 연결을 데이터베이스 연결성의 소스로서 사용한다.

  ``env.py`` 스크립트는 생성된 환경의 일부이기 때문에 마이그레이션이 작동되는 방식은
  완전히 커스터마이징이 가능하다. 연결 방식에 대한 정확한 설명과 마이그레이션 환경이
  실행되는 방식 또한 이 파일에 있다. 이 스크립트를 수정해서 여러 엔진이 사용되게 하고
  커스텀 인자를 마이그레이션 환경에 전달하고 어플리케이션 한정 라이브러리를 로드해서
  사용 가능하게 만들 수 있다.

  Alembic은 다른 사용 케이스들을 위한 각종 ``env.py`` 초기화 템플릿 세트를 포함하고 있다.
* ``README`` - 다양한 환경 템플릿에 함되어 있으며, 정보가 될 만한 것을 포함하고 있어야 한다.
* ``script.py.mako`` - 새로운 마이그레이션 스크립트를 생성할 때 사용되는
  `Mako <http://www.makotemplates.org>`_ 템플릿 파일이다.
  여기에 있는 것들은 ``versions/``\ 에 있는 새로운 파일을 생성하기 위해 사용된다.
  이 파일은 스크립트 가능하기 때문에 각 마이그레이션 파일의 구조는 제어될 수 있으며,
  각각의 내부에 있도록 표준 임포트를 포함시킬 수 있고 ``upgrade()``\ 와 ``downgrade()`` 함수의
  구조를 변경할 수도 있다. 예를 들어, ``multidb`` 환경은
  여러 함수가 ``upgrade_engine1()``, ``upgrade_engine2()``\ 를 사용해서
  생성되도록 할 수 있다.
* ``versions/`` - 이 디렉토리는 개별적인 버전 스크립트를 보관한다.
  다른 마이그레이션 도구의 사용자는 이 곳에 있는 파일이 증가하는 정수를 사용하지 않고
  대신 부분적인 GUID 접근을 사용하는 것을 알아차렸을 것이다. Alembic에서는 버전 스크립트의
  순서가 스크립트 자신이 포함된 디렉티브에 대해 상대적이며, 이론적으로 다른 버전 파일들을
  서로 잇는 것이 가능하고 다른 브랜치의 마이그레이션 시퀀스를 (비록 조심해야 하지만)
  수동으로 병합시킬 수 있다.


환경 생성하기(Creating an Environment)
======================================

환경이 무엇인지에 대한 기초적인 이해를 바탕으로, 우리는 ``alembic init``\ 을 사용해
환경을 생성할 수 있다. 이 명령은 "범옹" 템플릿을 사용해 환경을 생성한다::

    $ cd yourproject
    $ alembic init alembic

위에서, ``init`` 커맨드는 ``alembic``\ 이라고 하는 마이그레이션 디렉토리를 생성하기 위해 호출되었다::

    Creating directory /path/to/yourproject/alembic...done
    Creating directory /path/to/yourproject/alembic/versions...done
    Generating /path/to/yourproject/alembic.ini...done
    Generating /path/to/yourproject/alembic/env.py...done
    Generating /path/to/yourproject/alembic/README...done
    Generating /path/to/yourproject/alembic/script.py.mako...done
    Please edit configuration/connection/logging settings in
    '/path/to/yourproject/alembic.ini' before proceeding.

Alembic\ 은 또한 다른 환경 템플릿을 포함하고 있다. ``list_templates`` 커맨드를 사용하면
이 리스트르 볼 수 있다::

    $ alembic list_templates
    Available templates:

    generic - Generic single-database configuration.
    multidb - Rudimentary multi-database configuration.
    pylons - Configuration that reads from a Pylons project environment.

    Templates are used via the 'init' command, e.g.:

      alembic init --template pylons ./scripts

.ini 파일 편집하기(Editing the .ini File)
=========================================

Alembic\ 은 현재 디렉토리에 ``alembic.ini`` 파일을 만든다. 이 파일은 ``alembic`` 스크립트가
실행될 때 찾는 파일이다. 이 파일은 어디에 있어도 되는데 ``alembic`` 스크립트가 일반적으로 실행되는
디렉토리와 같은 디렉토리에 있거나, 다른 디렉토리에 있울 수도 있고 이 경우 ``alembic``\ 의
``--config`` 옵션을 사용해 디렉토리를 지정할 수 있다.

"generic" 설정으로 생성된 파일은 아래와 같다::

    # A generic, single database configuration.

    [alembic]
    # path to migration scripts
    script_location = alembic

    # template used to generate migration files
    # file_template = %%(rev)s_%%(slug)s

    # timezone to use when rendering the date
    # within the migration file as well as the filename.
    # string value is passed to dateutil.tz.gettz()
    # leave blank for localtime
    # timezone =

    # max length of characters to apply to the
    # "slug" field
    #truncate_slug_length = 40

    # set to 'true' to run the environment during
    # the 'revision' command, regardless of autogenerate
    # revision_environment = false

    # set to 'true' to allow .pyc and .pyo files without
    # a source .py file to be detected as revisions in the
    # versions/ directory
    # sourceless = false

    # version location specification; this defaults
    # to alembic/versions.  When using multiple version
    # directories, initial revisions must be specified with --version-path
    # version_locations = %(here)s/bar %(here)s/bat alembic/versions

    # the output encoding used when revision files
    # are written from script.py.mako
    # output_encoding = utf-8

    sqlalchemy.url = driver://user:pass@localhost/dbname

    # Logging configuration
    [loggers]
    keys = root,sqlalchemy,alembic

    [handlers]
    keys = console

    [formatters]
    keys = generic

    [logger_root]
    level = WARN
    handlers = console
    qualname =

    [logger_sqlalchemy]
    level = WARN
    handlers =
    qualname = sqlalchemy.engine

    [logger_alembic]
    level = INFO
    handlers =
    qualname = alembic

    [handler_console]
    class = StreamHandler
    args = (sys.stderr,)
    level = NOTSET
    formatter = generic

    [formatter_generic]
    format = %(levelname)-5.5s [%(name)s] %(message)s
    datefmt = %H:%M:%S

이 파일은 파이썬의 :class:`ConfigParser.SafeConfigParser` 객체를 사용해 읽어진다.
``%(here)s`` 변수는 대체 변수로서 제공되며, 예시에서 Alembic script location에 대해
한 것처럼 파일이나 디렉토리에 대한 절대 경로를 생성하려고 할 때 사용된다.

이 파일은 아래의 특징을 포함하고 있다:

* ``[alembic]`` - Alembic이 설정을 결정하는 데 쓰는 섹션이다.
  Alembic은 파일의 다른 부분을 직접 읽지 않는다. "alembic" 이름은 ``--name`` 커맨드라인
  플래그를 사용해서 커스터마이징 할 수 있다; 기초적인 예시는 :ref:`multiple_environments`\ 를
  참고하라.

* ``script_location`` - Alembic 환경의 위치를 가리킨다.
  일반적으로 상대 또는 절대 파일시스템의 위치로 지정된다. 위치가 상대 경로면
  현재 디렉토리에 상대적인 것으로 해석된다.

  이것은 모든 경우에 대해서 Alembic이 요구하는 유일한 키다.
  ``alembic init alembic`` 커맨드로 .ini 파일을 생성하면 자동적으로 이 디렉토리의
  이름을 ``alembic``\ 으로 설정한다. 특수 변수 ``%(here)s`` 또한 ``%(here)s/alembic``
  처럼 사용될 수 있다.

  자신을 .egg 파일로 패키징하는 어프리케이션 지원을 위해,
  값은 `package resource <https://pythonhosted.org/setuptools/pkg_resources.html>`_\ 로도
  지정될 수 있다, 이 경우 파일을 찾기 위해 ``resource_filename()``\ 이 사용된다. (0.2.2에
  추가). 모든 콜론을 포함하는 비-절대 URI는 파일이름 자체보다 리소스 이름으로 해석된다.

* ``file_template`` - 새로운 마이그레이션 파일을 생성하기 위해 사용되는 네이밍 스키마다.
  this is the naming scheme used to generate new migration files.
  현재 값이 디폴트이므로, 코멘트처리된다. 사용가능한 토큰은 아래와 같다:

    * ``%%(rev)s`` - 리비전 id
    * ``%%(slug)s`` - 리비전 메세지에서 파생된 짧게 변형된 문자열
    * ``%%(year)d``, ``%%(month).2d``, ``%%(day).2d``, ``%%(hour).2d``,
      ``%%(minute).2d``, ``%%(second).2d`` - 생성 날짜의 구성요소,
      ``timezone`` 설정 옵션이 사용되지 않으면 디폴트로
      ``datetime.datetime.now()``\ 를 사용한다.

* ``timezone`` - 선택적인 시간대 이름(예시, ``UTC``, ``EST5EDT`` 등)으로
  마이그레이션 파일의 코멘트 내부와 파일명에서 렌더링되는 타임스탬프에 적용된다.
  ``timezone``\ 이 지정되면, 생성 날짜 객체는 ``datetime.datetime.now()``\ 에서
  파생되지 않는 대신에 아래처럼 생성된다::

      datetime.datetime.utcnow().replace(
            tzinfo=dateutil.tz.tzutc()
      ).astimezone(
          dateutil.tz.gettz(<timezone>)
      )

  .. versionadded:: 0.9.2

* ``truncate_slug_length`` - 디폴트는 40, "slug" 필드에서 포함하는 문자의 최대 수.

  .. versionadded:: 0.6.1 - ``truncate_slug_length`` 설정 추가됨.

* ``sqlalchemy.url`` - SQLAlchemy를 통해 데이터베이스에 연결하기 위한 URL.
  이 키는 사실 "generic" 설정에 한정된 ``env.py`` 파일 내에서만 참조된다;
  파일은 개발자가 커스터마이징할 수 있다. 다중 데이터베이스 설정은 이곳의 다중 키에 대응,
  시키거나 파일의 다른 섹션을 참조하게 할 수 있다.

* ``revision_environment`` - 'true'로 설정되면 마이그레이션 환경 스크립트
  ``env.py``\ 가 새 리비전 파일을 생성할 때와 ``alembic history``\ 을 실행할 때
  무조건 적으로 실행되게 지시한다.

  .. versionchanged:: 0.9.6 ``revision_environment``\ 이 true로 설정되었을 때
     ``alembic history`` 커맨드가 무조건적으로 환경을 이용한다.

* ``sourceless`` - 'true'\ 로 설정되면, versions 디렉토리에 .pyc 또는 .pyo
  파일 존재하는 리비전 파일만 버전으로 사용될 것이며 "sourceless"가
  폴더를 버저닝 하는 것을 허용한다. 디폴트인 'false'으로 되어 있으면 ,
  버전 파일로 .py 파일만 버전 파일로 사용된다.

  .. versionadded:: 0.6.4

* ``version_locations`` - 선택적인 리비전 파일 위치의 리스트,
  리비전이 동시에 여러 디렉토리에 존재하는 것을 허용한다.
  예시는 :ref:`multiple_bases`\ 를 참고하라.

  .. versionadded:: 0.7.0

* ``output_encoding`` - Alembic이 ``script.py.mako``\ 파일로 새로운 마이그레이션
  파일을 작성할 때 사용하는 인코딩. 디폴트는 ``'utf-8'``\ 이다.

  .. versionadded:: 0.7.0

* ``[loggers]``, ``[handlers]``, ``[formatters]``, ``[logger_*]``, ``[handler_*]``,
  ``[formatter_*]`` - 이 섹션은 파이썬의 기본 표준 로깅 설정의 모든 파드다, 메커니즘에
  설명은 `Configuration File Format <http://docs.python.org/library/logging.config.html#configuration-file-format>`_\ 에
  나와있다. 데이터베이스 커넥션의 경우처럼, 이 디렉티브는 마음대로 수정할 수 있는 ``env.py``
  스크립트에 있는 ``logging.config.fileConfig()`` 호출의 결과로서 직접 사용된다.

단일 데이터베이스와 범옹 설정으로 시작하는 경우, SQLAlchemy URL만 세팅해주면 된다::

    sqlalchemy.url = postgresql://scott:tiger@localhost/test


.. _create_migration:

마이그레이션 스크립트 생성(Create a Migration Script)
=====================================================

환경이 준비되면 ``alembic revision``\ 을 사용해 새로운 리비전을 생성할 수 있다::

    $ alembic revision -m "create account table"
    Generating /path/to/yourproject/alembic/versions/1975ea83b712_create_accoun
    t_table.py...done

``1975ea83b712_create_account_table.py``\ 이 생성됐다. 파일 내부를 보자::

    """create account table

    Revision ID: 1975ea83b712
    Revises:
    Create Date: 2011-11-08 11:40:27.089406

    """

    # revision identifiers, used by Alembic.
    revision = '1975ea83b712'
    down_revision = None
    branch_labels = None

    from alembic import op
    import sqlalchemy as sa

    def upgrade():
        pass

    def downgrade():
        pass

파일은 헤더 정보와 현재 버전과 "downgrade" 리비전에 대한 식별자, 기본 Alembic
디렉티브 임포트, 빈 ``upgrade()``, ``downgrade()`` 함수를 포함하고 있다.
우리가 할 일은 ``upgrade()``\ 와 ``downgrade()`` 함수를 데이터베이스에 변경사항을
적용시키는 디렉티브로 채우는 것이다.
일반적으로 ``upgrade()``\ 가 필요하며 ``downgrade()``\ 는 리비전을
다운시켜야 할 필요가 요구되는 경우에만 필요하지만 작성해두는 것이 좋다.

또 주의해야할 것은 ``down_revision`` 변수다. 이 변수는 Alembic이
마이그레이션을 적용시키는 정확한 순서를 인식하는 방식이다. 새로운 리비전을 생성할 때,
새로운 파일의 ``down_revision`` 식별자는 위 리비전을 가리키게 된다::

    # revision identifiers, used by Alembic.
    revision = 'ae1027a6acf'
    down_revision = '1975ea83b712'

Alembic는 ``versions/`` 디렉토리에 대해 작업을 할 때마다 디렉토리 안에 있는 모든
파일을 읽고 ``down_revision``\ 이 ``None``\ 으로 된 파일을 시작으로 해서
``down_revision`` 식별자가 어떻게 연결되어 있는지에 기반해 리스트를 구성한다.
이론적으로 마이그레이션 환경이 많은 마이그레이션을 가지고 있으면, 시작할 때 약간의
대기시간이 추가될 수 있지만 실제로는 프로젝트에서 오래된 마이그레이션을 제거해는 것이
좋다. (현재 데이터베이스를 완전히 빌드할 수 있도록 유지하면서 이런 식으로 하는 방법은
설명은 :ref:`building_uptodate`\ 를 참고하라.)

그 다음에 스크립트에 디렉티브를 추가한다. 새로운 테이블 ``account``\ 를 추가한다고
가정해보자::

    def upgrade():
        op.create_table(
            'account',
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('name', sa.String(50), nullable=False),
            sa.Column('description', sa.Unicode(200)),
        )

    def downgrade():
        op.drop_table('account')

:meth:`~.Operations.create_table`\ 과 :meth:`~.Operations.drop_table`\ 는
Alembic 디렉티브다. Alembic은 이 간단하고 미니멀한 디렉티브들을 통해서
기본적인 모든 데이터베이스 마이그레이션 작업을 제공한다;
대부분의 디렉티브는 현존하는 테이블 메타데이터에 의존하지 않는다.
이 디렉티브들은 명령을 실행하기 위해 데이터베이스에 대한 연결을 나타내는
전역 "컨텍스트"를 사용한다. (만약에 있다면, 마이그레이션dms SQL/DDL
디렉티브를 파일에도 덤핑할 수 있다.
전역 컨텍스트는 다른 것들과 마찬가지로 ``env.py`` 스크립트에서 설정된다.

모든 Alembic 디렉티브에 대한 개요는 :ref:`ops`\ 를 참고하라.

첫 번째 마이그레이션 실행하기(Running our First Migration)
==========================================================

이제 마이그레이션을 실행할 것이다. 데이터베이스는 완전히 깨끗하고 아직 버저닝되지
않았다고 가정하자. ``alembic upgrade`` 커맨드는 업그레이드 작업을 실행할 것이고,
현재 버전, 지금 예제에서는 ``None``\ 에서 부터 주어진 목표 리비전으로 진행이 될 것이다.
``1975ea83b712``\ 을 리비전으로 지정했으므로 이 버전으로 업그레이드 할 것이지만,
대부분의 경우에 "가장 최신" 리비전으로 하라고 명령하는 것(이 경우는, ``head``)이 더 쉽다::

    $ alembic upgrade head
    INFO  [alembic.context] Context class PostgresqlContext.
    INFO  [alembic.context] Will assume transactional DDL.
    INFO  [alembic.context] Running upgrade None -> 1975ea83b712

스크린에 보이는 정보는 ``alembic.ini``\ 에 있는 로깅 설정의 결과다
- ``alembic`` 스트림을 콘솔에 로깅하도록 했다(특히, 표준 에러).

첫 번째 과정은 Alembic이 데이터베이스에 ``alembic_version``\ 이라는 테이블이
있는지 체크하고 없으면 만드는 것이다. 이 테이블에서 현재 버전을 찾고, 있으면
이 버전과 요청된 버전의 경로를 게산한다. 이 경우는 ``head``\ 이며
``1975ea83b712``\ 로 인식된다. 그 다음 목표 리비전에 도달하기 위해 각 파일에
있는 ``upgrade()`` 메서드를 실행시킨다.

두 번째 마이그레이션 실행하기(Running our Second Migration)
===========================================================

좀 더 가지고 놀아보자. 다시 리비전 파일을 생성했다::

    $ alembic revision -m "Add a column"
    Generating /path/to/yourapp/alembic/versions/ae1027a6acf_add_a_column.py...
    done

파일을 편집하고 새로운 컬럼을 ``acount`` 테이블에 추가했다::

    """Add a column

    Revision ID: ae1027a6acf
    Revises: 1975ea83b712
    Create Date: 2011-11-08 12:37:36.714947

    """

    # revision identifiers, used by Alembic.
    revision = 'ae1027a6acf'
    down_revision = '1975ea83b712'

    from alembic import op
    import sqlalchemy as sa

    def upgrade():
        op.add_column('account', sa.Column('last_transaction_date', sa.DateTime))

    def downgrade():
        op.drop_column('account', 'last_transaction_date')

다시 ``head``\ 로 실행시켜 보자::

    $ alembic upgrade head
    INFO  [alembic.context] Context class PostgresqlContext.
    INFO  [alembic.context] Will assume transactional DDL.
    INFO  [alembic.context] Running upgrade 1975ea83b712 -> ae1027a6acf

이제 데이터베이스에 ``last_transaction_date`` 컬럼이 추가되었다.

부분적인 리비전 식별자(Partial Revision Identifiers)
====================================================

리비전 숫자를 명시적으로 참고할 필요가 있는 때가 있는데, Alembic은
부분적인 숫자를 사용할 수 있는 옵션이 있다. 이 숫자가 제대로 버전을
식별할 수만 있으면, 모든 커맨드에서 버전 숫자가 필요한 모든 위치에 이 방식을
사용할 수 있다.

    $ alembic upgrade ae1

위에서, ``ae1027a6acf`` 리비전을 참조하기 위해  ``ae1``\ 를 사용했다.
Alembic은 프리픽스로 시작하는 버전이 한 개 이상 있을 경우 동작을 중지하고
사용자에게 알려줄 것이다.

.. _relative_migrations:

상대적 마이그레이션 식별자(Relative Migration Identifiers)
==========================================================

상대적인 업그레이드/다운그레이드 또한 제공된다.
현재 버전에서 두 버전을 이동하려면 십진수 값 "+N"을 사용하면 된다::

    $ alembic upgrade +2

다운그레이드는 음수값을 사용하면 된다::

    $ alembic downgrade -1

상대적 식별자는 특정한 리비전이 될 수도 있다. 예를 들어 ``ae1027a6acf``\ 에
추가적인 두 스텝을 더하고 싶으면 아래와 같이 사용하면 된다::

    $ alembic upgrade ae10+2

.. versionadded:: 0.7.0 특정한 리비전에 대한 상대적 마이그레이션 지원

정보 얻기(Getting Information)
==============================

몇 가지 리비전이 존재하기 때문에 상태에 대한 몇 가지 정보를 얻을 수 있다.

첫째로 현재 리비전을 볼 수 있다::

    $ alembic current
    INFO  [alembic.context] Context class PostgresqlContext.
    INFO  [alembic.context] Will assume transactional DDL.
    Current revision for postgresql://scott:XXXXX@localhost/test: 1975ea83b712 -> ae1027a6acf (head), Add a column

``head``\ 는 데이터베이스의 리비전 식별자가 헤드 리비전과 일치할 때만
 표시된다.

또한 ``alembic history``\ 로 히스토리를 볼 수 있다; ``--verbose`` 옵션은
(``history``, ``current``, ``heads``, ``branches``\ 를 포함해 여러 커맨드에서
허용이 가능하며) 각 리비전에 대한 전체 정보를 보여줄 것이다::

    $ alembic history --verbose

    Rev: ae1027a6acf (head)
    Parent: 1975ea83b712
    Path: /path/to/yourproject/alembic/versions/ae1027a6acf_add_a_column.py

        add a column

        Revision ID: ae1027a6acf
        Revises: 1975ea83b712
        Create Date: 2014-11-20 13:02:54.849677

    Rev: 1975ea83b712
    Parent: <base>
    Path: /path/to/yourproject/alembic/versions/1975ea83b712_add_account_table.py

        create account table

        Revision ID: 1975ea83b712
        Revises:
        Create Date: 2014-11-20 13:02:46.257104

히스토리 범위 보기(Viewing History Ranges)
------------------------------------------

``-r`` 옵션을 ``alembic history``\ 에 사용하면, 히스토리를 잘라서 볼 수 있다.
``-r`` 인자는 ``[start]:[end]`` 값을 받는데, 이 값은 리비전 숫자나 ``head``, ``heads`` 또는
``base``,  현재 리비전을 지정하는 ``current`` 심볼을 사용할 수 있으며
``[start]``\ 에 상대적인 음수 범위 ``[end]``\ 에 상대적인 양수 범위를
사용할 수도 있다::

  $ alembic history -r1975ea:ae1027

이전의 세 리비전부터 현재 마이그레이션으로 지정된 상대 범위는 현재 마이그레이션을
얻기 위해 데이터베이스에 마이그레이션 환경을 실행시킨다::

  $ alembic history -r-3:current

1975 부터 헤드까지의 모든 리비전을 보기::

  $ alembic history -r1975ea:

.. versionadded:: 0.6.0  ``alembic revision``\ 는 버전 숫자, 심볼, 상대적 델타를
   기반으로한 특정한 범위를 지정하기 위한 ``-r`` 인자를 받는다.


다운그레이딩(Downgrading)
=========================

``alembic downgrade``\ 를 호출해서 Alembic에서 ``base``\ 라고 불리는 아무것도 없던 상태,
시작 시점으로 다운그레이드 할 수있다::

    $ alembic downgrade base
    INFO  [alembic.context] Context class PostgresqlContext.
    INFO  [alembic.context] Will assume transactional DDL.
    INFO  [alembic.context] Running downgrade ae1027a6acf -> 1975ea83b712
    INFO  [alembic.context] Running downgrade 1975ea83b712 -> None

아무것도 없던 상태에서 다시 최신 상태로 업그레이드::

    $ alembic upgrade head
    INFO  [alembic.context] Context class PostgresqlContext.
    INFO  [alembic.context] Will assume transactional DDL.
    INFO  [alembic.context] Running upgrade None -> 1975ea83b712
    INFO  [alembic.context] Running upgrade 1975ea83b712 -> ae1027a6acf

다음 단계(Next Steps)
=====================

대다수의 Alembic 환경은 "autogenerate" 기능을 많이 사용한다.
계속해서 다음 섹션, :doc:`autogenerate`\ 으로 진행하라.
