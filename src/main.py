from os import (
        path,
        listdir,
        mkdir,
    )
from shutil import (
        copy,
        rmtree,
    )
from markdown import (
        extract_title,
        generate_page,
        generate_pages_recursively,
    )

def file_looper(directory=""):
    public_path = path.dirname(__file__)+"/../public"
    static_path = path.dirname(__file__)+"/../static"
    for file in listdir(static_path+"/"+directory):
        if path.isfile(static_path+"/"+directory+"/"+file):
            copy(static_path+"/"+directory+"/"+file, public_path+"/"+directory+"/"+file)
        else:
            mkdir(public_path+"/"+directory+"/"+file)
            file_looper(directory+"/"+file)

def copy_static():
    public_path = path.dirname(__file__)+"/../public"
    if path.exists(public_path):
        rmtree(public_path)
    mkdir(public_path)
    file_looper()

def main():
    copy_static()
    project_dir = path.dirname(__file__)+"/.."
    generate_pages_recursively(project_dir+"/content", project_dir+"/template.html", project_dir+"/public")


if __name__=="__main__":
    main()
