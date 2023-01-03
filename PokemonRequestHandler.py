import requests
import sqlite3
from datetime import datetime, timedelta
import random
import math
import discord

class PokemonRequestHandler:
    def __init__(self):
        self.db = sqlite3.connect('pokemonbot')
        self.cursor = self.db.cursor()

    async def spawn(self, e):
        self.cursor.execute('''
            INSERT OR IGNORE INTO Users(ID, lastDropTime) VALUES(?, NULL)''', (e.author.id,))
        
        self.cursor.execute('''
            SELECT lastDropTime FROM Users WHERE ID = ?
        ''', (e.author.id, ))
        
        date = self.cursor.fetchone()[0]
        if date != None:
            currentDate = datetime.now()
            dateCheck = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f') + timedelta(minutes = 15)
            if currentDate > dateCheck:
                randomNum = random.randint(1, 905)
                response = requests.get('http://pokeapi.co/api/v2/pokemon/' + str(randomNum))
                pokemon = response.json()
                self.cursor.execute('''
                    INSERT INTO Pokemon(userID, pokemonName, pokemonID) VALUES(NULL, ?, ?)
                ''', (pokemon.get('name'), pokemon.get('id')))
                self.db.commit()
                self.cursor.execute('''
                    SELECT * FROM Pokemon
                ''')
                embed = discord.Embed(
                    title = pokemon.get('name'),
                    description = pokemon.get('id')
                )
                embed.set_image(url = pokemon.get('sprites').get('front_default'))
                msg = await e.channel.send(embed = embed)
                await msg.add_reaction('😺')
            else:
                timedifference = currentDate - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
                await e.reply(str(math.ceil((900-timedifference.total_seconds())/60)) + ' minutes till next spawn')
        
        else:
            currentDate = datetime.now()
            self.cursor.execute('''
                UPDATE Users
                SET lastDropTime = ?
                WHERE ID = ?
            ''', (currentDate, e.author.id,))
            self.db.commit()
            randomNum = random.randint(1, 905)
            response = requests.get('http://pokeapi.co/api/v2/pokemon/' + str(randomNum))
            pokemon = response.json()
            self.cursor.execute('''
                INSERT INTO Pokemon(userID, pokemonName, pokemonID) VALUES(NULL, ?, ?)
            ''', (pokemon.get('name'), pokemon.get('id')))
            self.db.commit()
            self.cursor.execute('''
                SELECT * FROM Pokemon
            ''')
            embed = discord.Embed(
                title = pokemon.get('name'),
                description = pokemon.get('id')
            )
            embed.set_image(url = pokemon.get('sprites').get('front_default'))
            msg = await e.channel.send(embed = embed)
            await msg.add_reaction('😺')

    async def claim(self, reaction, user, bot):
        if(user.id != bot.user.id):
            pokemonID = reaction.message.embeds[0].description
            self.cursor.execute('''
                UPDATE Pokemon
                SET userID = ?
                WHERE pokemonID = ?
            ''', (user.id, int(pokemonID)))
            self.cursor.execute('''
                SELECT * FROM Pokemon
            ''')
            self.db.commit()

    async def showCollection(self, e):
        self.cursor.execute('''
            SELECT * FROM Pokemon WHERE userID = ?
        ''', (e.author.id, ))
        collection = self.cursor.fetchall()
        embed = discord.Embed()
        collectionString = ''
        for i, pokemon in enumerate(collection):
            collectionString += f'{i+1}. ' + pokemon[2] + '\n'
        embed.add_field(name = 'Collection', value = collectionString, inline = False)
        await e.channel.send(embed = embed)

    async def showOne(self, e, index):
        self.cursor.execute('''
            SELECT * FROM Pokemon WHERE userID = ?
        ''', (e.author.id, ))
        pokemon = self.cursor.fetchall()
        pokemon = pokemon[int(index)-1]
        response = requests.get('http://pokeapi.co/api/v2/pokemon/' + str(pokemon[3]))
        json = response.json()
        embed = discord.Embed(
            title = pokemon[2],
            description = pokemon[3]
        )
        embed.set_image(url = json.get('sprites').get('front_default'))
        msg = await e.channel.send(embed = embed)

    async def deleteOne(self, e, index):
        self.cursor.execute('''
            SELECT * FROM Pokemon WHERE userID = ?
        ''', (e.author.id, ))
        collection = self.cursor.fetchall()
        pokemon = collection[int(index)-1]
        self.cursor.execute('''
            DELETE FROM Pokemon WHERE ID = ?
        ''', (int(pokemon[0]),))
        self.db.commit()