document.getElementById('capture').addEventListener('click',function(){
    context = canvas.getContext('2d')
    context.drawImage(video,0,0,400,300);

});