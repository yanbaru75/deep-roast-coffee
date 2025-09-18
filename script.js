/** 小さなJS: 営業中表示とモバイルナビ **/
(function(){
  var s = document.getElementById('openState');
  if(s){
    var now = new Date();
    var open = new Date(now); open.setHours(9,0,0,0);
    var close = new Date(now); close.setHours(18,0,0,0);
    if(now < open || now > close){
      s.textContent = '本日は閉店中 09:00-18:00';
      s.style.color = '#a00';
    }
  }
  var burger = document.querySelector('.hamburger');
  var nav = document.querySelector('.nav');
  if(burger && nav){
    burger.addEventListener('click', function(){
      var open = nav.style.display === 'flex';
      nav.style.display = open ? 'none' : 'flex';
      burger.setAttribute('aria-expanded', (!open).toString());
    });
  }
})();
