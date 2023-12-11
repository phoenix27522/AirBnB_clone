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
        """Updates an instance by adding or updating attribute."""
        if arg == "" or arg is None:
            print("** class name missing **")
            return

        rex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match = re.search(rex, arg)
        className = match.group(1)
        uid = match.group(2)
        attr = match.group(3)
        value = match.group(4)
        if not match:
            print("** class name missing **")
        elif className not in storage.classes():
            print("** class doesn't exist **")
        elif uid is None:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(className, uid)
            if key not in storage.all():
                print("** no instance found **")
            elif not attr:
                print("** attribute name missing **")
            elif not value:
                print("** value missing **")
            else:
                patch = None
                if not re.search('^".*"$', value):
                    if '.' in value:
                        patch = float
                    else:
                        patch = int
                else:
                    value = value.replace('"', '')
                attribute = storage.attributes()[className]
                if attr in attribute:
                    value = attribute[attr](value)
                elif patch:
                    try:
                        value = patch(value)
                    except ValueError:
                        pass
                setattr(storage.all()[key], attr, value)
                storage.all()[key].save()

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
