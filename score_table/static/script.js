const form = document.querySelector('#rankingForm');
const rankingTable = document.querySelector('#rankingTable');

async function fetchRankingData() {
    try {
        let response = await fetch('/api/rankings');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        let data = await response.json();
        console.log(data);
        return data;
    } catch (error) {
        console.error('fetch error:', error);
    }
}


// ISO 8601 から YYYY/MM/DD HH:MM の形式に変換する関数
function format_date(isoDate) {
    const dateObj = new Date(isoDate);
    const year = dateObj.getFullYear();
    const month = String(dateObj.getMonth() + 1).padStart(2, '0');
    const day = String(dateObj.getDate()).padStart(2, '0');
    const hours = String(dateObj.getHours()).padStart(2, '0');
    const minutes = String(dateObj.getMinutes()).padStart(2, '0');
    const formattedDate = `${year}/${month}/${day} ${hours}:${minutes}`;
    return formattedDate;
}

async function displayRanking() {
    let rankingData = await fetchRankingData();
    console.log(rankingData);
    rankingTable.innerHTML = ''; 

    rankingData.forEach((entry, i) => {
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>${i + 1}</td>
        <td>${entry.name}</td>
        <td>${entry.score}</td>
        <td>${format_date(entry.date)}</td>`;
        rankingTable.appendChild(row);
    });
}

displayRanking();


setTimeout(function(){
    window.location.reload();
}, 60000); 


