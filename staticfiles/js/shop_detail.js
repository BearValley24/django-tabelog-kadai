//予約フォームにoption要素を入れ込む　日
const optionYoyaku1 = document.getElementById('yoyaku_form1');

//定休日を表示
var regularHoliday = document.getElementById('regularHoliday');
var rgh = regularHoliday.getAttribute('rgh');
if (rgh === '7' || rgh === ''){
  rgh = '7'
}
const daysMap = {
  '0':'日曜日',
  '1':'月曜日',
  '2':'火曜日',
  '3':'水曜日',
  '4':'木曜日',
  '5':'金曜日',
  '6':'土曜日',
  '7':'定休日無し',
};
document.getElementById('regularHoliday').textContent = daysMap[String(rgh)];

//現在の年月日を取得
var now = new Date();
var nowYear = now.getFullYear();
var nowMonth = now.getMonth() +1;
var nowDate = now.getDate();

if (nowMonth < 10){
  var nowMonth = '0' + nowMonth
};

if (nowDate < 10){
  var nowDate = '0' + nowDate
};

var nowYMD = nowYear + '-' + nowMonth + '-' + nowDate;
if (now.getDay() != rgh){
  option = document.createElement('option');
  option.value = nowYMD;
  option.textContent = nowYMD;
  optionYoyaku1.appendChild(option);
};
//現在から14日後の年月日を取得 予約フォームにoption要素を入れ込む
let plusYMD = {};
for (let i = 1; i < 15; i++){
  var plusNow = new Date()
  plusNow.setDate(plusNow.getDate() + i); 
  var plusYear = plusNow.getFullYear();
  var plusMonth = plusNow.getMonth() + 1;
  var plusDate = plusNow.getDate();
  if (plusMonth < 10){
    var plusMonth = '0' + plusMonth
  };
  if (plusDate < 10){
    var plusDate = '0' + plusDate
  };
  plusYMD[i] =  plusYear + '-' + plusMonth + '-' + plusDate;
  if (plusNow.getDay() === Number(rgh)){
    continue;
  };
  option = document.createElement('option');
  option.value = plusYMD[i];
  option.textContent = plusYMD[i];
  optionYoyaku1.appendChild(option);
}

//予約フォームにoption要素を入れ込む　時
const optionYoyaku2 = document.getElementById('yoyaku_form2');


//営業時間の取得 予約時点では予約開始時間だけ決めさせる　終了時間は店次第
var worktimeLunch = document.getElementById('worktimeLunch');
var wtl_start = worktimeLunch.getAttribute('wtl_start');
var wtl_end = worktimeLunch.getAttribute('wtl_end') ;
var worktimeDinner = document.getElementById('worktimeDinner');
var wtd_start = worktimeDinner.getAttribute('wtd_start');
var wtd_end = worktimeDinner.getAttribute('wtd_end');

//営業終了時刻の1時間前まで30分ごと追加
if (wtl_start != null) {
  var wtl_end_min = new Date(nowYMD + 'T' + wtl_end);
  wtl_end_min.setHours(wtl_end_min.getHours() - 1);
  option = document.createElement('option');
  option.value = wtl_start;
  option.textContent = wtl_start;
  optionYoyaku2.appendChild(option);

  var plusTime = new Date(nowYMD + 'T' + wtl_start);
  var j = 1;
  do {
    plusTime.setMinutes(plusTime.getMinutes() + 30);
    //console.log(plusTime)
    // 時間と分を取得し、2桁に整える
    var hours = plusTime.getHours();
    var minutes = plusTime.getMinutes();

    // 分が1桁なら先頭に '0' を付ける
    if (minutes < 10) {
      minutes = '0' + minutes;
    }
    // 時が1桁なら先頭に '0' を付ける
    if (hours < 10) {
      hours = '0' + hours;
    }

    // 'hh:mm' 形式でオプションに追加
    var formattedTime = hours + ':' + minutes;
    
    option = document.createElement('option');
    option.value = formattedTime;
    option.textContent = formattedTime;
    optionYoyaku2.appendChild(option);
    if (plusTime >= wtl_end_min){
      break;
    };
    j = j + 1;
  }while(j < 20);
};
if (wtd_start != null) {
  var wtd_end_min = new Date(nowYMD + 'T' + wtd_end);
  wtd_end_min.setHours(wtd_end_min.getHours() - 1);
  option = document.createElement('option');
  option.value = wtd_start;
  option.textContent = wtd_start;
  optionYoyaku2.appendChild(option);

  var plusTime = new Date(nowYMD + 'T' + wtd_start);
  var j = 1;
  do {
    plusTime.setMinutes(plusTime.getMinutes() + 30);
    //console.log(plusTime)
    // 時間と分を取得し、2桁に整える
    var hours = plusTime.getHours();
    var minutes = plusTime.getMinutes();

    // 分が1桁なら先頭に '0' を付ける
    if (minutes < 10) {
      minutes = '0' + minutes;
    }
    // 時が1桁なら先頭に '0' を付ける
    if (hours < 10) {
      hours = '0' + hours;
    }

    // 'hh:mm' 形式でオプションに追加
    var formattedTime = hours + ':' + minutes;
    
    option = document.createElement('option');
    option.value = formattedTime;
    option.textContent = formattedTime;
    optionYoyaku2.appendChild(option);
    if (plusTime >= wtd_end_min){
      break;
    };
    j = j + 1;
  }while(j < 20);
};

