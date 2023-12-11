#!/usr/bin/python3
"""Defines the HBnB console."""

import cmd
import re
from models.base_model import BaseModel
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
            sp_brac = split(args[:bracket.span()[0]])
            list_t = [i.strip(",") for i in sp_brac]
            list_t.append(curley_brace.group())
            return list_t
    else:
        sp_curly = split(args[:curley_brace.span()[0]])
        list_t = [i.strip(",") for i in sp_curly]
        list_t.append(curley_brace.group())
        return list_t


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter."""

    prompt = "(hbnb) "
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
            print("** class name missing **")
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
            print("** class doesn't exist **")
        elif "{}.{}".format(arg[0], arg[1]) not in sto_file:
            print("** no instance found **")
        else:
            print(sto_file["{}.{}".format(arg[0], arg[1])])

    def do_destroy(self, args):
        """destroy the class instance"""
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

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        replace = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match_dot = re.search(r"\.", arg)
        if match_dot:
            command, args = arg.split(".", 1)
            match_bracket = re.search(r"\((.*?)\)", args)
            if match_bracket:
                command_name = args[:match_bracket.start()].strip()
                command_args = args[
                    match_bracket.start() + 1:match_bracket.end() - 1]
                if command_name in replace:
                    return replace[command_name](f"{command} {command_args}")
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_count(self, args):
        """Counts the number of instances of a specified class.

        Args:
            args (str): The class name for which the instances are counted.

        Prints the count of instances of the specified class.
        """
        class_name = args.strip()
        count = 0
        all_objects = storage.all().values()
        for obj in all_objects:
            if type(obj).__name__ == class_name:
                count += 1
        print(count)


if __name__ == "__main__":
    HBNBCommand().cmdloop()
