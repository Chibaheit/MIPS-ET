path = require 'path'
fs = require 'fs'
express = require 'express'
app = express()
http = require('http').Server(app)
io = require('socket.io')(http)
$ = window.$

rootPath = path.normalize __dirname + '/..'
app.use express.static rootPath

http.listen 8080

