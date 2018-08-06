# Datadog

Master: [![Build Status](https://travis-ci.org/sansible/datadog.svg?branch=master)](https://travis-ci.org/sansible/datadog)
Develop: [![Build Status](https://travis-ci.org/sansible/datadog.svg?branch=develop)](https://travis-ci.org/sansible/datadog)

* [ansible.cfg](#ansible-cfg)
* [Installation and Dependencies](#installation-and-dependencies)
* [Tags](#tags)
* [Examples](#examples)

This roles installs the Datadog agent.

The agent service is intentionally disabled on bootup; during boot a machine
will most likelyconsume a high amount of resourc es whilst the OS and all of
its services start which will trip any CPU or Memory usage alarms erroneously.


## Installation and Dependencies

To install run `ansible-galaxy install sansible.datadog` or add this to your
`roles.yml`.

```YAML
- name: sansible.datadog
  version: v2.0
```

and run `ansible-galaxy install -p ./roles -r roles.yml`




## Tags

This role uses one tag: **build**

* `build` - Installs Datadog and all its dependencies.
* `configure` - Configures datadog and install integrations




## Integrations

The `datadog/templates/conf.d` directory contains the implemented integrations.
The majority of them are self explanatory.

### DNS Check

Sample data structure for DNS Check integration:

```YAML
roles:
  - role: sansible.datadog
    sansible_datadog_integrations:
      dns_check:
        default_timeout: 1
        checks:
          - name: "Some Domain"
            hostname: "some.domain.com"
            nameserver: "127.0.0.1"
          - name: "Some Other Domain"
            hostname: "some.other.domain.com"
            nameserver: "10.1.1.2"
```

### Gunicorn

For Gunicorn integration you need to supply a list of app names to be
monitored, please see [https://docs.datadoghq.com/integrations/gunicorn/]()
for more information on how to setup DataDog and Gunicorn.

```YAML
roles:
  - role: sansible.datadog
    sansible_datadog_integrations:
      gunicorn:
        app_names:
          - my_app
          - another_app
    sansible_datadog_tags:
      - my_app
      - role:my_app
```

### TCP Check

Sample data structure for TCP Check integration.

```YAML
roles:
  - role: sansible.datadog
    sansible_datadog_integrations:
      tcp_check:
        - endpoint: "my.domain.com"
          name: "TCP Check for my.domain.com"
          port: "443"
        - endpoint: "your.domain.com"
          name: "TCP Check for your.domain.com"
          port: "80"
          timeout: 2
          collect_response_time: "false"
          min_collection_interval: 60
      sansible_datadog_tags:
        - some_app
        - role:some_app
```


## Examples

To install:

```YAML
- name: Install and Configure Datadog
  hosts: "somehost"

  roles:
    - role: sansible.datadog
```

Setup Datadog with some integrations and tags:

```YAML
- name: Install and Configure Datadog
  hosts: "somehost"

  roles:
    - role: sansible.datadog
      sansible_datadog_integrations:
        php_fpm: {}
        nginx: {}
      sansible_datadog_tags:
        - some_app
        - role:some_app
```

You can disable the agent completely if desired, this can be used to build
images that have DD installed with the option turn DD off in certain
environments where monitoring is not needed (eg. dev or scratch environments):

```YAML
# Environment var file eg. vars/dev/vars.yml

sansible_datadog_enabled: no
```

```YAML
- name: Install and configure Datadog
  hosts: "somehost"

  vars_files:
    - vars/dev/vars.yml

  roles:
    - role: sansible.datadog
```

**Note** This behaviour requires `hash_behaviour` to be set to `merge`.

By default this role will start the DD agent in the [tasks/configure.yml] task
file, this behaviour can be disabled however if you wish to start the agent
within another role:

```YAML
- name: Install and Configure Datadog
  hosts: "somehost"

  vars_files:
    - vars/dev/vars.yml

  roles:
    - role: sansible.datadog
      sansible_datadog_autostart_agent: no

    # The task of this role will be be to start the DD agent service
    role: my_service_role
```

Using .default_tags to set global tags, these get blended with .tags:

```YAML
# Environment var file eg. vars/dev/vars.yml

sansible_datadog_default_tags:
  - environment:dev
```

```YAML
- name: Install and Configure Datadog
  hosts: "somehost"

  vars_files:
    - vars/dev/vars.yml

  roles:
    - role: sansible.datadog
      sansible_datadog_tags:
        - some_app
        - role:some_app
```

**Note** This behaviour requires `hash_behaviour` to be set to `merge`.

This will result in the following tags:

```
- environment:dev
- some_app
- role:some_app
```

Disable Datadog service (useful for disabling in some environments):

```YAML
- name: Install and Configure Datadog
  hosts: "somehost"

  roles:
    - role: sansible.datadog
      sansible_datadog_enabled: false
```
