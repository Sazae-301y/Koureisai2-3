const form = document.getElementById('rankingForm');
const rankingTable = document.getElementById('rankingTable');

let editMode = false;
const editBtn = document.querySelector('.edit');
const confirmDiv = document.querySelector('.confirm');
let rankingData = JSON.parse(localStorage.getItem('ranking')) || [];

// ranking data
function displayRanking() {
    rankingTable.innerHTML = ''; // reset table

    // Sort data by score
    rankingData.sort((a, b) => b.score - a.score);

    rankingData.forEach((entry, i) => {
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>${i + 1}</td>
        <td>${entry.name}</td>
        <td>${entry.score}</td>
        <td>${entry.date}</td>
        <td class="delete_td hidden">
            <button onclick="confirmDelete(${i})">削除</button>
        </td>`;
        rankingTable.appendChild(row);
    });
}

//press the edit button
editBtn.addEventListener('click', () => {
    let items = document.querySelectorAll('.delete_td');
    if (editMode) {
        items.forEach(item => {
            item.classList.remove('hidden');
        });
        editMode = !editMode;
    } else {
        items.forEach(item => {
            item.classList.add('hidden');
        });
        editMode = !editMode
    }
});
// realy dlete??function
async function confirmDelete(index) {
    confirmDiv.classList.remove('hidden');
    result = await waitForYesOrNo();
    if (result === 'yes') {
        deleteEntry(index);
    };  
    confirmDiv.classList.add('hidden');
}
function waitForYesOrNo() {
    return new Promise(resolve => {
        yes.addEventListener('click', () => resolve('yes'), { once: true });
        no.addEventListener('click', () => resolve('no'), { once: true });
    });
}
// delate raking
function deleteEntry(index) {
    rankingData.splice(index, 1); // 指定したインデックスのデータを削除
    localStorage.setItem('ranking', JSON.stringify(rankingData)); // 更新されたデータを保存
    displayRanking(); // 更新後のランキングを表示
    editBtn.click();
}

// フォームの送信イベントリスナー
form.addEventListener('submit', function (event) {
    event.preventDefault();

    // 入力されたデータを取得
    const name = document.getElementById('name').value;
    const score = document.getElementById('score').value;
    const date = new Date().toLocaleString();

    // ランキングデータに追加
    rankingData.push({ name, date, score });

    // データをlocalStorageに保存
    localStorage.setItem('ranking', JSON.stringify(rankingData));

    // フォームをリセット
    form.reset();

    // ランキングを表示
    displayRanking();
});

// show the ranking, lol page
displayRanking();