# Base telegram bot template

## Boilerplate for start to develop telegram bot using [aiogram 3.x](https://github.com/aiogram/aiogram) and also

### To work with the database
- [sqlalchemy](https://github.com/sqlalchemy/sqlalchemy)+[alembic](https://github.com/sqlalchemy/alembic) as orm and migration management

### To interact with the blockchain ton
- [pytonconnect](https://github.com/XaBbl4/pytonconnect) for connect users wallets using ton connect v2
- [pytonapi](https://github.com/tonkeeper/pytonapi) for parsing the necessary data from the blockchain
- [pytoniq](https://github.com/yungwine/pytoniq) to work with blockchain primitives and communicate with the blockchain via adnl protocol

### For the realization scheduled tasks
- [apscheduler](https://github.com/agronholm/apscheduler) - to perform scheduled tasks asynchronously


## Don't forget
```commandline
mkdir alembic/versions
mkdir bot/connections
```

## Deploy bot on server
To deploy the bot to the server you need to upload the folder with the ready bot to the server, then upload the configuration file [bot.service](bot.service) for autostart and autorestart bot to the `etc/systemd/system/` folder, having previously configured it.
Then execute the commands:

```commandline
sudo systemctl daemon-reload
sudo systemctl enable bot
sudo systemctl start bot
sudo systemctl status bot
```


## TODO

- add CI/CD
- add tests
