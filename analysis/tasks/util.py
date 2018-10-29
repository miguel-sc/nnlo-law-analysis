def createRuncard(baseRuncard, params):

  if (params['channel'] == 'RRa'):
    channel = 'RR'
    region = 'a'
  elif (params['channel'] == 'RRb'):
    channel = 'RR'
    region = 'b'
  else:
    channel = params['channel']
    region = 'all'

  substitutions = {
    '@SEED@': params['seed'],
    '@WARMUP@': params['warmup'],
    '@PRODUCTION@': params['production'],
    '@EVENTS@': params['events'],
    '@ITERATIONS@': params['iterations'],
    '@FULLCHANNEL@': params['channel'],
    '@CHANNEL@': channel,
    '@REGION@': region,
    '@UNIT_PHASE@': params['unit_phase']
  }

  data = baseRuncard

  for key, value in substitutions.iteritems():
    data = data.replace(key, value)

  return data
