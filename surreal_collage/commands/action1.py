from enum import IntEnum

from surreal_collage.log import logger

def create_action1_parser(subparser):
  parser = subparser.add_parser(
    "action1", help="Perform the dummy 'action1'"
  )

  parser.add_argument('--arg1', help='some string', default='asdfghjk')
  parser.add_argument('stuff', help='list of stuff to pass in', nargs='+')
  parser.add_argument('--style', default='none', help='how to process the stuff', choices=['none', 'swagger', 'haste', 'butter'])
  parser.add_argument('--force', action='store_true', help='use the force')

  # Here set the function that should be run for this action
  parser.set_defaults(func = run_action1)

def run_action1(args):
  # use the args, do some logging
  if len(args.stuff) == 0:
    logger.warning('Hey, you did not pass any stuff!')
  else:
    logger.info(' '.join(args.stuff))
  logger.info('This is the entry point 1 of surreal_collage')
  if args.force:
    logger.info('Using the force, with %r', args.style)
