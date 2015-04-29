app = require 'app'
BrowserWindow = require 'browser-window'
menu = require 'menu'
tray = require 'tray'
menuItem = require 'menu-item'

mainWindow = null

somethingWindow = null

app.on 'window-all-closed', ->
  app.quit() if process.platform isnt 'darwin'

app.on 'ready', ->
  mainWindow = new BrowserWindow
    height: 675
    width: 600
    'web-preferences':
      'webgl': true
  mainWindow.loadUrl "file://#{__dirname}/index.html"
  ###
  mainWindow.openDevTools
    detach: true
  somethingWindow.openDevTools
    detach: true
  ###
  appIcon = new tray "#{__dirname}/assets/img/tray.png"
  appMenu = new menu
  aboutWindow = new BrowserWindow
    show: false
    height: 675
    width: 600
    'web-preferences':
      'webgl': true
  aboutWindow.loadUrl "file://#{__dirname}/about.html"
  show = new menuItem
    type: 'normal'
    label: 'show'
    click: ->
      mainWindow.show()
  
  hide = new menuItem
    type: 'normal'
    label: 'hide'
    click: ->
      mainWindow.hide()
  
  about = new menuItem
    type: 'normal'
    label: 'about'
    click: ->
      aboutWindow.show()
  
  exit = new menuItem
    type: 'normal'
    label: 'exit'
    click: ->
      aboutWindow.close true
      mainWindow.close true
  appMenu.append show
  appMenu.append hide
  appMenu.append about
  appMenu.append exit
  
  appIcon.setContextMenu appMenu 
           
  
  mainWindow.on 'closed', ->
    mainWindow = null