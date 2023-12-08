#!/usr/bin/python3
"""Defines the HBnB console."""

import cmd
import re
from models import storage
from shlex import split
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


def parse(args):
    """Parses the provided string argument into a list
       based on enclosed curly braces or square brackets.

    Args:
    - args (str): A string containing arguments possibly
                  enclosed in curly braces '{}' or square brackets '[]'.

    Returns:
    - list: A list of parsed arguments stripped
            of commas and enclosing brackets.
    """
    curley_brace = re.search(r"\{(.*?)\}", args)
    bracket = re.search(r"\[(.*?)\]", args)

    if curley_brace is None:
        if bracket is None:
            return [i.strip(",") for i in split(args)]
        else:
            sp_brac = args[:bracket.span()[0]].split(',')
            list_t = [i.strip(",") for i in sp_brac]
            list_t.append[bracket.group()]
            return list_t
    else:
        sp_curly = args[:curley_brace.span()[0]].split(',')
        list_t = [i.strip(",") for i in sp_curly]
        list_t.append[curley_brace.group()]
        return list_t


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter."""

    prompt = "(hbnb)"
    __commands = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Amenity",
        "Place",
        "Review"
    }

    def emptyline(self):
        """Do nothing in this condition"""
        pass

    def do_EOF(self, args):
        """Signal for exit"""
        print("")
        return True

    def do_quit(self, args):
        """QUIT command to exit"""
        return True

    def do_create(self, args):
        """Creats a new instance of the BaseModel"""
        arg = parse(args)
        if len(arg) == 0:
            print("** class doesn't exist **")
        elif arg[0] not in HBNBCommand.__commands:
            print("** class doesn't exist **")
        else:
            print(eval(arg[0])().id)
            storage.save()

    def do_show(self, args):
        """ shows the instance when invoked """
        arg = parse(args)
        sto_file = storage.all()

        if len(arg) == 0:
            print("** class name missing **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif arg[0] not in HBNBCommand.__commands:
            print("** class dosen't exist **")
        elif "{}.{}".format(arg[0], arg[1]) not in sto_file:
            print("** no insatnce found **")
        else:
            print(sto_file["{}.{}".format(arg[0], arg[1])])

    def do_destroy(self, args):
        """destroy the class instance"""
        arg = parse(args)
        sto_file = storage.all()

        if len(arg) == 0:
            print("** class name missing")
        elif len(arg) == 1:
            print("** instance id is missing **")
        elif arg[0] not in HBNBCommand.__commands:
            print("** class doesn't exist **")
        elif "{}.{}".format(arg[0], arg[1]) not in sto_file:
            print("** no instance found **")
        else:
            del sto_file["{}.{}".format(arg[0], arg[1])]
            storage.save()

    def do_all(self, args):
        """Prints all instances based or not on the class name"""
        arg = parse(args)
        sto_file = storage.all()

        if len(arg) == 0:
            print([str(val) for val in sto_file.values()])
        elif arg[0] not in HBNBCommand.__commands:
            print("** class doesn't exist **")
        else:
            print([
                str(val)
                for key, val in sto_file.items()
                if key.startswith(arg[0])
                ])

    def do_update(self, args):
        """Updates an instance based on the class name and id"""
        arg = parse(args)
        sto_file = storage.all()

        if len(arg) == 0:
            print("** class name missing **")
        elif len(arg) == 1:
            print("** instance id missing **")
        elif arg[0] not in HBNBCommand.__commands:
            print("** class doesn't exist **")
        elif "{}.{}".format(arg[0], arg[1]) not in sto_file:
            print("** no instance found **")
        elif len(arg) == 2:
            print("** attribute name missing **")
        elif len(arg) == 3:
            print("** value missing **")
        else:
            instance_key = "{}.{}".format(arg[0], arg[1])
            instance = sto_file[instance_key]
            setattr(instance, arg[2], arg[3])
            instance.save()
            storage.save()

    def default(self, args):
        replace = {
            "all": self.do_all,
        }
        match = re.search(r"\.(\w+)\((.*?)\)", args)
        if match:
            method = match.group(1)
            params = match.group(2)
            if method in replace:
                # Call the respective method with parameters
                return replace[method](params)
        print("*** Unknown syntax: {}".format(args))
        return False


if __name__ == "__main__":
    HBNBCommand().cmdloop()
