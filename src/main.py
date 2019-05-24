from make_variables import MakeVariables 

def main():
    path_dict = MakeVariables('HTI', 2016)
    print(path_dict.variables_paths['ann_composite'].exists())


if __name__ == "__main__":
    main()

