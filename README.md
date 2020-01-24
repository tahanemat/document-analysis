# document-analysis
Extract all dates from provided PDF file or PNG file

After cloning repository, please run:
```
docker-compose up
```

This should start 3 docker services (flask app, rabbitmq and extractor app)

Please note:

The extractor app is written in C# so it immediately exits when running within the same terminal as the other services.
In order to work around this, open a separate terminal, stop extractor app container and start it in interactive mode in the new terminal.

