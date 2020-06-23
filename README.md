# Data analysis
- Name of project: catchafish
- Description: Fish Identification tool
- Data Source: http://groups.inf.ed.ac.uk/f4k/GROUNDTRUTH/RECOG/?fbclid=IwAR3Mi2Nxar3W8xe-DZGWJWgP5_jnrIHcxryGVqIv7ecN4ZHV6v-HoQCbYMc
- Type of analysis: Image Recognition



# Stratup the project

The initial setup.

Create virtualenv and install the project:
```bash
  $ sudo apt-get install virtualenv python-pip python-dev
  $ deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
  $ make clean install test
```

Check for catchafish in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/catchafish`
- Then populate it:

```bash
  $ ##   e.g. if group is "{group}" and project_name is "catchafish"
  $ git remote add origin git@gitlab.com:{group}/catchafish.git
  $ git push -u origin master
  $ git push -u origin --tags
```

Functionnal test with a script:
```bash
  $ cd /tmp
  $ catchafish-run
```
# Install
Go to `gitlab.com/{group}/catchafish` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:
```bash
  $ sudo apt-get install virtualenv python-pip python-dev
  $ deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:
```bash
  $ git clone gitlab.com/{group}/catchafish
  $ cd catchafish
  $ pip install -r requirements.txt
  $ make clean install test                # install and test
```
Functionnal test with a script:
```bash
  $ cd /tmp
  $ catchafish-run
```

# Continus integration
## Github
Every push of `master` branch will execute `.github/workflows/pythonpackages.yml` docker jobs.
## Gitlab
Every push of `master` branch will execute `.gitlab-ci.yml` docker jobs.
