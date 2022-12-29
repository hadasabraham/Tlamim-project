


function searchInDatabase(){
    let searchBar = document.getElementById("searchBarInput");
    const cond = searchBar.value;
    searchBar.value = "";
    fetchAllCandidatesByCond(cond).then(r => {});
}

async function fetchAllCandidatesByCond(cond){
    const urlServer = 'http://127.0.0.1:8001/candidates/query/' + cond;
    let response = await fetch(urlServer);
    const data = await response.json();
    renderDataInTheTable(data);
}



function renderDataInTheTable(data) {
    const old_tbody = document.getElementById("candidatesTableBody");
    let new_tbody = document.createElement('tbody');
    old_tbody.parentNode.replaceChild(new_tbody, old_tbody); // clear the table body
    new_tbody.setAttribute("id", "candidatesTableBody");

    data.forEach(record => {
        let row = document.createElement("tr")
        Object.values(record).forEach((value) => {
            let cell = document.createElement("td");
            cell.innerText = value;
            cell.classList.add('td-sm', 'text-center', 'border')
            row.appendChild(cell);
        })
        new_tbody.appendChild(row)
    })

}