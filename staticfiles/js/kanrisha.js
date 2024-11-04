var now = new Date();
var nowYear = now.getFullYear();
var nowMonth = now.getMonth() +1;

// 年に自動的に現在の年を入力
const inputY = document.getElementById('inputYear');
inputHTML = document.createElement('input');
inputHTML.type = 'search';
inputHTML.size = '4';
inputHTML.name = 'inputYear';
inputHTML.value = nowYear;
inputY.appendChild(inputHTML);

// 月のoptionを生成し現在月をデフォルトで選択する
const inputM = document.getElementById('inputMonth');

  // 選択無し
  option = document.createElement('option');
  option.value = 'all';
  option.textContent = '';
  inputM.appendChild(option);
  // 1~12月
  for (let i = 1; i < 13; i++){
    option = document.createElement('option');
    option.value = i
    option.textContent = i
    if (i === nowMonth) {
      option.selected = true 
    };
    inputM.appendChild(option);
  };
  
// 日のoptionを生成し現在月をデフォルトで選択する
const inputD = document.getElementById('inputDate');
var now = new Date();
var nowDate = now.getDate();

  // 選択無し
  option = document.createElement('option');
  option.value = 'all';
  option.textContent = '';
  inputD.appendChild(option);
  // 1~31日
  for (let i = 1; i < 32; i++){
    option = document.createElement('option');
    option.value = i
    option.textContent = i
    if (i === nowDate) {
      option.selected = true 
    };
    inputD.appendChild(option);
  };

