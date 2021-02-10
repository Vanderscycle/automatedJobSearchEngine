#!/bin/bash
source ~/miniconda2/etc/profile.d/conda.sh # Remove the following 3 lines if not needed
DESIRED_ENV=NNScraper
conda activate $DESIRED_ENV 
# add actions (later) because we are going the DevOps CI/CD route
function gitFiles(){
    # -f for file -d for directoy
    if [ ! -d .github ]
    then
        # -p for parents
        mkdir actions-a
        mkdir -p .github/workflows
        echo 'Created the workflows and actions-a folders'
    fi

    if [ ! -f README.md ]
    then
        touch README.md
        echo 'README.md file created'
    fi

    if [ ! -f .gitignore ]
    then
        touch .gitignore
        echo '.gitignore file created'
        #EOL sometimes gives you errors if there is a space after
        cat >> .gitignore << EOL
newRepo.sh
.ipynb_checkpoints
.log
__pycache__
.vscode
.env
EOL
    fi

    if [ ! -f .env ]
    then
        touch .env
        echo 'Empty .env file created'
    fi
}

# Dockerfile/.dockerignore/requirements.txt (requires pipreqs)
function dockerFiles(){

    if [ ! -f Dockerfile ]
    then
        touch Dockerfile
        echo 'Empty Dockerfile file created'
        cat >> Dockerfile << EOL
FROM 
LABEL maintainer "Henri Vandersleyen <hvandersleyen@gmail.com>"
EOL
    fi

    if [ ! -f .dockerignore ]
    then
        touch .dockerignore
        echo '.dockerignore file created'
        cat >> .dockerignore << EOL
Dockerfile
.ipynb_checkpoints
.log
__pycache__
.vscode
.env
EOL
    fi
    
    echo 'Creating the requirements.txt file'
    pipreqs . #pip install pipreqs # if not installed on your machine
    read -p 'Do you want to keep the python module version in requirements.txt? [y/n]': YSNOANS
    case $YSNOANS in
        [yY] | [yY][eE][sS])
        echo 'Removing the python module version'
        # using sed to remove the version of each file -i flag updates the file name
        sed -i 's/==.*//' requirements.txt
        ;;
        [nN] | [nN][oO])
        echo 'NIL changes to requirements.txt'
        ;;
    esac
}
echo 'Welcome to the automatic Git and Docker files creation tool'
echo 'If you want to init a new git repo with an already populated .gitignore, partially populated README.md and empty .env file?: git'
echo 'If you want to init a new Docker with a partialy populated Dockerfile, populated .dockerignore file and a automatically generated requirements.txt?: docker'
echo 'If you want to create both Git and Docker file please senter: both'
read -p 'What do you want to create? (git/docker/both)': ANSWER

case $ANSWER in
    [gG] | [gG][iI][tT]) #g or git
        echo 'Creating git files'
        gitFiles
        ;;
    [dD] | [dD][oO][cC][kK][eE][rR])
        echo 'Creating docker files'
        dockerFiles
        ;;
    [bB] | [bB][oO][tT][hH])
        echo 'Creating both git and docker files'
        gitFiles
        dockerFiles
        ;;
    *)
        echo 'Please enter g/git, d/docker or b/both'
esac
read -p 'Do you want to init a new repo': ANSWERGIT

case $ANSWERGIT in
    [yY] | [yY][eE][sS])
    echo 'creating the repo'
    if [ ! -d .git ]
    then
        git init
    fi
    git add *
    git commit -a -m 'first commit'
    git branch -M main 
    read -p 'What is the GitHub address?': ADDRESS
    git remote add origin $ADDRESS
    echo 'pushing first commit to main'
    git push -u origin main
    git config --global credential.helper wincred
    git pull
    ;;
    [nN] | [nN][oO])
    echo 'No new repo created'
    ;;
esac