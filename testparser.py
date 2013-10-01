#!/usr/bin/env python

import sys, argparse, string

teststrings = [ "delete t1", "delete", "delete -t t1 t2", "list t1", "", "list" ]

def delete_things(args):
	if args.testing:
		print "Only testing"
	else:
		print "Not testing"
	print string.join(args.playlists, ", ")

def list_things(args):
	print "Listing things, no arguments taken"
	print args

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_delete = subparsers.add_parser("delete")
parser_delete.add_argument("-t", "--testing", help="If in testing mode, no changes are made to YouTube playlists", action="store_true")
parser_delete.add_argument("playlists", metavar="playlist", nargs='+', help="playlists to process")
parser_delete.set_defaults(func=delete_things)

parser_list = subparsers.add_parser("list")
parser_list.set_defaults(func=list_things)

if 0:
	for ts in teststrings:
		print "Running parser with '%s'" % ts
		try:
			args, unknown = parser.parse_known_args(ts.split())
			args.func(args)
		except:
			pass
		print

# TODO why does making this just "known_args" result in 
# TypeError: 'Namespace' object is not iterable
args, unknown = parser.parse_known_args()
args.func(args)