# Simpler cookie-cutter
This is my version of the [Cookie-cutter Data Science project](https://drivendata.github.io/cookiecutter-data-science/). I initially started using that project, but got confused and tangle with a lot of concepts I do not know. I couldn't find a step-by-step example using that project, so I decided to take a step back, and lay a project structure that makes sense to me and my work methodology. I suspect the complications I didn't understand from the original project are in part due to my inexperience, and in part due to the project's intention to cater to a broad audience, which adds overhead complexity, unnecessary for the uninitiated (🙋‍♂️).


# Start here: Things you will want to change
There are a few changes we need to apply to adapt this template to a new project. Once you have downloaded or cloned this repo please follow these steps: 

## Project name
Change the name of the project directory folder to a name that makes sense with your project:
1. Project directory name: current name is simplified_project_cookiecutter

## Conda environment name
This template assumes you are using conda for managing environments. The environment name is defined in a few places that you'll need to modify (they should all have the same value):

2. `environment.yml`: Current environment name is set with `name: my_env_name`

3. `tasks.py`: Current environment name is set with `ENV_NAME = 'my_env_name'`

4. `Makefile`: Current environment name is set with `PROJECT_NAME = my_env_name`

## Package name
By default we create a Python package named `src` by defining the `setup.py` and by adding it as a dependency to the `environment.yml file`. If you would like your package to have a different name you can change the file:

5. `setup.py`: Current package name is set with `name='src'`

## Author name
The author name appears in a couple of places:

1. `setup.py`: Currently set with `author='Rafael Pinto'`
2. `LICENSE`: Currently on the third line. You might want to choose a different [license for your project](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/licensing-a-repository)


# Set conda environment
After tailoring the environment and project names with the instructions above we are ready to start working the project. First we will set up the conda environment. Then we will see how to use invoke to update our environment.

## Check the initial dependencies
Check that the `environment.yml` file has the regular libraries that you will need to start a project. I've added a few that I find useful, but you can add or remove as you please. My current workflow uses invoke, papermill, and python-dotenv, so if you want to follow along you will need those.

## The need for `invoke`
Open the `task.py` file. Here we record a set of useful commands for setting and updating the conda environment. In addition, you will define your workflow's key execution steps on this file. I think of `task.py` as a substitute for the `Makefile`. I was happily using `make` until I had to start developing on Windows.

`make` comes preloaded in almost all OS X systems, but not on Windows. Installing it on Windows is not a trivial task, specially without elevated privileges. Therefore, I'll use `invoke`, as it is Python native, and provides similar functionality as what I need from `make`. The latter is still on this template if you prefer that. Just pick one and stick to it.

## Create and activate conda environment
Now we are ready to create the conda environment. This and the environment activation are the only steps that can't be added as a task to the `tasks.py` file:

> For consistency use the same environment name that you set on the **Conda environment name** section above. Replace `my_env_name` in the code below with your environment name.

On a terminal window:
```shell
conda env create --name my_env_name --file environment.yml
conda activate my_env_name
```

## Set up Jupyter
With the environment activated we can run our first task for setting up a named Jupyter kernel, and for adding notebook extensions (time cell, table of content, word highlighting).

On the project directory run:
```shell
invoke env-set-jupyter
```

> Note that the syntaxt uses kebab-case and not snake_case.

## Freeze environment
We will use a two YAML file strategy for keeping track of dependencies:

1. `environment.yml`: Built by hand for humans. Comes with this template. Keeps a manageable list of dependencies. You will want to add new dependencies here.

2. `environment_to_freeze.yml`: It is built from the current activated environment using `invoke env-to-freeze` (that is `conda env export` behind the scenes) for computers. It is meant to keep a detailed list of your dependencies, and their respective dependencies, so anyone can reproduce your conda environment with `invoke env-update`.

At this point we are ready to create our first `environment_to_freeze.yml` file:

```shell
invoke env-to-freeze
```

## Add or remove dependencies to your conda environment
Since this is a common task, I added the `invoke env-update` command. Suppose you want to add `scikit-learn`:

1. Add `scikit-learn` to your `environment.yml` file.
2. Update the environment. On a terminal run: `invoke env-update`
3. Freeze the environment. On a terminal run: `invoke env-to-freeze`

Now `scikit-learn` is in both of your YAML files.


# How to operate
With the conda environment set up we are ready to start working. This is a general workflow that I follow, and that I have seen recommended (at least some aspects of it) by [other people that write code](https://www.youtube.com/watch?v=yXGCKqo5cEY&t=64s).

The developing workflow can be summarized as follows:

1. Write your exploratory code in a Jupyter notebook. This code is exploratory because most of the time we don't have a requirements specification before starting to write, instead we are primarily concerned with understanding what is in the data, and how to cleaning it and make inferences from it.
2. Once you are happy with one step of the exploratory code (e.g. fixing the data column names), abstract your exploratory code into a function or class method, place it on the respective module (e.g. src/data/utils.py), and refactor your notebook to use this function (`from src.data.utils import fix_col_names`). Don't wait until you have completed the entire exploratory analysis to do this. It is best if it is done after each key step while your mind is still focused on this problem.
3. Write unit test for the function or class method you just wrote on step two. This will enable repurposing your functions further down the development path while minimizing the possibility of breaking the code for which these functions were originally intended to.
4. Cycle trough steps 1 to 3 until the particular task is completed, e.g. `clean_data` generally fixes column names, assigns proper data types to columns, provides a summary of statistics for each column, and removes duplicated rows and columns.
5. You have effectively constructed one or many notebooks that do one step of the data analysis. You would like to document what notebooks need to be run to complete this step. For this, we need to write a task on the `task.py` file using `papermill`.

The workflow above will give you code and data exploration flexibility, while also allowing you to explicitly define the critical steps on the `task.py`. In this manner, we are documenting all of our steps, which makes it easier for another person or your future self to understand what you did, and be able to follow and reproduce your work.


# Conventions
Having everyone on the team following the workflow above will tremendously help in making the work reproducible. Still, there are so many ways one can program the same task and organize the work that it is best to have a common set of conventions.

## Project directory structure
I borrowed this structure from [cookie-cutter data science](https://github.com/drivendata/cookiecutter-data-science/blob/master/README.md) and adapted it to my own structure. Essentially, I left out directories and files I have never worked with, and added the use of `invoke` as a substitute for `make`. Also, I changed the data directories definitions.

I found confusing having all these empty directories and files created at once before starting the project. As a result, this template only provides the bare minimum, leaving the flexibility to create the rest of the directories to you when needed.

```
├── LICENSE
├── Makefile           <- Makefile with commands like `make data` or `make train`
├── task.py            <- Execute key steps with commands like `invoke data` or `invoke train`
├── README.md          <- The top-level README for developers using this project.
├── data
│   ├── external       <- The original, immutable data dump.
│   ├── raw            <- The external data after cleaning step.
│   ├── interim        <- Intermediate data that has been transformed.
│   └── processed      <- The final, canonical data sets for modeling. 
│
├── models             <- Trained and serialized models, model  predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description,
│                         e.g. `1.0-jqp-initial-data-exploration`.
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│
├── environment.yml    <- The dependencies tracking file for reproducing the analysis environment, e.g.
│                         generated by hand.
│
├── environment_to_freeze.yml    <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `conda env export --name ENV_NAME --file environment_to_freeze.yml`
│
├── src                <- Source code for use in this project.
│   ├── __init__.py    <- Makes src a Python module
│   │
│   ├── definitions.py <- Keep project singletons, e.g. `ROOT_DIR`
│   │
│   ├── data           <- Scripts to download or generate data
│   │   ├── utils.py   <- Keep common data wrangling functions.
│   │   └── make_dataset.py
│   │
│   ├── features       <- Scripts to turn raw data into features for modeling
│   │   └── build_features.py
│   │
│   ├── models         <- Scripts to train models and then use trained models to make
│   │   │                 predictions
│   │   ├── predict_model.py
│   │   └── train_model.py
│   │
│   └── visualization  <- Scripts to create exploratory and results oriented visualizations
│       └── visualize.py

```

## Notebooks naming
Again, borrowing the idea from cookie-cutter data science, we should use:

> Naming convention is a number (for ordering), the creator's initials, and a short `-` delimited description, e.g. `1.0-jqp-initial-data-exploration`.

## Define project working directory as a singleton
Many of your notebooks will have references to the data in the project directory. If you use relative paths and then move the notebook to a different directory the data links will break. A way to prevent this is by defining the project directory as a singleton variable in the `src/definitions.py` file. This is already included on this template, so in your code you can do `from src.definitions import ROOT_DIR` which points to the project's root path. This is a `Path` object from the `pathlib` library so you can operate on it as follows:

```python
data_filename = ROOT_DIR / r'data/raw/my_raw_data.csv'
```
Note that the forward slash (`/`) will work in both OS X and Windows systems. 🙂

## Data pipeline
I struggled for some time with the definition of the data directories in cookie-cutter data science template. My main quarrel is with the definitions of external and raw:

1. External: Data from third party sources.
2. Raw: The original, immutable data dump.

> Isn't all input data external?

> And if so, shouldn't it be treated as original and immutable data dump?

With this questions in mind I redefine these terms as:

1. External: All incoming data, to be treated as original and immutable data dump. 
2. Raw: The external data after cleaning step.

And so we end up with a nice progression of data directories that hint at the readiness status of the files contained therein:

> external > raw > interim > processed

The idea is that after each major step we save the transformed data on the appropriate directory, and the pick it up from there on subsequent notebooks, e.g.:

1. All data downloaded of shared with us goes in the external directory.
2. Once we clean the external data we can save it on the raw directory. This will probably be a pickled `pandas DataFrame`.
3. The interim directory will hold the data where:
   - Null values have been dealt with (row drop or imputation)
   - The data has been scaled and transformed as needed.
4. The processed directory will contain the final, canonical data sets for modeling.

## Working with secrets
There are a couple different ways to safely deal with secrets. One is to keep them as [conda environment variables](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#setting-environment-variables). This requires adding your secrets to a conda environment file outside the current project directory. On the other hand, we can create a `.env` file in the project directory containing the secrets, and then use `python-dotenv` to retrieve them in our working script. The latter approach is described in detail in [cookie-cutter data science](https://drivendata.github.io/cookiecutter-data-science/#keep-secrets-and-configuration-out-of-version-control) and it is what we will use.
 
