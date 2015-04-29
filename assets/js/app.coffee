exec = require('child_process').exec
shell = require 'shell'

asmHolder = document.getElementById 'asm-holder'
asmHolder.ondragover = ->
  return false
asmHolder.ondragleave = asmHolder.ondragend = ->
  return false
asmHolder.ondrop = (e) ->
  e.preventDefault()
  asmFile = e.dataTransfer.files[0].path
#  console.log "python #{__dirname}/asm/asm.py " + asmFile 
  if $('input[name="my-checkbox"]').bootstrapSwitch('state') == true
    console.log "python #{__dirname}/asm/asm.py " + asmFile + " -f coe"
    exec "python #{__dirname}/asm/asm.py " + asmFile + " -f coe", (error, stdout, stderr) ->
  #    console.log error
  #    console.log stdout
      alert stdout if error?
  #    alert "nya"
      return false if error?
      asmNotification = new window.Notification 'Transfer successed!'
      shell.openExternal "file://#{stdout}" if !(error?)
    return false  
  else
    exec "python #{__dirname}/asm/asm.py " + asmFile + " -f bin", (error, stdout, stderr) ->
  #    console.log error
  #    console.log stdout
      alert stdout if error?
  #    alert "nya"
      return false if error?
      asmNotification = new window.Notification 'Transfer successed!'
      shell.openExternal "file://#{stdout}" if !(error?)
    return false      

reasmHolder = document.getElementById 'reasm-holder'
reasmHolder.ondragover = ->
  return false
reasmHolder.ondragleave = reasmHolder.ondragend = ->
  return false
reasmHolder.ondrop = (e) ->
  e.preventDefault()
  reasmFile = e.dataTransfer.files[0].path
#  console.log "python #{__dirname}/asm/asm.py " + asmFile
  exec "python #{__dirname}/reasm/reasm.py " + reasmFile, (error, stdout, stderr) ->
#    console.log error
#    console.log stdout
    alert stdout if error?
#    alert "nya"
    return false if error?
    reasmNotification = new window.Notification 'Transfer successed!'
    shell.openExternal "file://#{stdout}" if !(error?)
  return false 
  
$ ->
  # Foundation.global.namespace = ''
  # $(document).foundation()
  $('#fullpage').fullpage
    sectionsColor: ['#1bbc9b', '#4BBFC3']
    anchors: ['first', 'second']
    menu: '#menu'
    css3: true
    scrollingSpeed: 1000

