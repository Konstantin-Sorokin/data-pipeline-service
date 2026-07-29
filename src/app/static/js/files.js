let currentPage = 1;
let pageSize = 50;

let selectedIds = new Set();
let selectedAll = false;

let currentPageIds = [];


const filesTable = document.getElementById("files-table");
const calculateButton = document.getElementById("calculate");

const selectAllCheckbox = document.getElementById("select-all");
const selectPageCheckbox = document.getElementById("select-page-checkbox");

const statisticsBlock = document.getElementById("statistics");


async function loadFiles(page = 1) {

    currentPage = page;


    const response = await fetch(
        `/api/files?page=${page}&page_size=${pageSize}`
    );


    const data = await response.json();


    renderFiles(data.items);

    renderPagination(data);

}


function renderFiles(files) {

    filesTable.innerHTML = "";


    currentPageIds = files.map(
        file => file.id
    );


    files.forEach(file => {


        const row = document.createElement("tr");


        let statisticsCells = "";


        for (let digit = 0; digit <= 9; digit++) {

            statisticsCells += `
                <td>
                    ${file.statistics[digit]}
                </td>
            `;
        }


        row.innerHTML = `

            <td>
                <input
                    type="checkbox"
                    class="file-checkbox"
                    data-id="${file.id}"
                >
            </td>


            <td>
                ${file.name}
            </td>


            <td>
                ${formatDate(file.downloaded_at)}
            </td>


            ${statisticsCells}

        `;


        filesTable.appendChild(row);

    });


    updateCheckboxes();

    updatePageCheckbox();

    bindCheckboxes();

}


function bindCheckboxes() {


    document
        .querySelectorAll(".file-checkbox")
        .forEach(checkbox => {


            checkbox.addEventListener(
                "change",
                () => {


                    const id = Number(
                        checkbox.dataset.id
                    );


                    if (checkbox.checked) {

                        selectedIds.add(id);

                    } else {

                        selectedIds.delete(id);

                        selectedAll = false;

                        selectAllCheckbox.checked = false;
                    }


                    updatePageCheckbox();

                }
            );


        });

}


function updateCheckboxes() {


    document
        .querySelectorAll(".file-checkbox")
        .forEach(checkbox => {


            const id = Number(
                checkbox.dataset.id
            );


            checkbox.checked =
                selectedAll ||
                selectedIds.has(id);


        });


}


function updatePageCheckbox() {


    if (currentPageIds.length === 0) {
        return;
    }


    const selectedOnPage =
        currentPageIds.filter(
            id => selectedIds.has(id)
        ).length;


    selectPageCheckbox.checked =
        selectedOnPage === currentPageIds.length;


    selectPageCheckbox.indeterminate =
        selectedOnPage > 0 &&
        selectedOnPage < currentPageIds.length;

}


selectAllCheckbox.addEventListener(
    "change",
    () => {


        selectedAll =
            selectAllCheckbox.checked;


        if (selectedAll) {

            selectedIds.clear();

        }


        updateCheckboxes();

        updatePageCheckbox();

    }
);


selectPageCheckbox.addEventListener(
    "change",
    () => {


        if (selectPageCheckbox.checked) {


            currentPageIds.forEach(id => {

                selectedIds.add(id);

            });


        } else {


            currentPageIds.forEach(id => {

                selectedIds.delete(id);

            });


            selectedAll = false;

            selectAllCheckbox.checked = false;

        }


        updateCheckboxes();

    }
);


calculateButton.addEventListener(
    "click",
    async () => {


        if (
            !selectedAll &&
            selectedIds.size === 0
        ) {

            alert(
                "Выберите файлы"
            );

            return;

        }


        const body = selectedAll

            ? {
                all_files: true
            }

            : {
                file_ids: Array.from(selectedIds),
                all_files: false
            };


        const response = await fetch(
            "/api/statistics",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(body)

            }
        );


        const data =
            await response.json();


        if (!response.ok) {

            alert(data.detail);

            return;

        }


        renderStatistics(
            data.statistics
        );

    }
);


function renderStatistics(statistics) {


    statisticsBlock.innerHTML = "";


    for (const digit in statistics) {


        const row =
            document.createElement("div");


        row.textContent =
            `Цифра ${digit}: ${statistics[digit]}`;


        statisticsBlock.appendChild(row);

    }

}


function renderPagination(data) {


    const pagination =
        document.getElementById(
            "pagination"
        );


    pagination.innerHTML = "";


    const totalPages =
        Math.ceil(
            data.total / data.page_size
        );


    addPageButton(
        "← Назад",
        data.page - 1,
        data.page > 1,
        pagination,
        data.page
    );


    let pages = [];


    if (totalPages <= 5) {

        pages = Array.from(
            {length: totalPages},
            (_, i) => i + 1
        );


    } else if (data.page <= 3) {

        pages = [
            1,
            2,
            3,
            "...",
            totalPages
        ];


    } else if (data.page >= totalPages - 2) {

        pages = [
            1,
            "...",
            totalPages - 2,
            totalPages - 1,
            totalPages
        ];


    } else {

        pages = [
            1,
            "...",
            data.page,
            "...",
            totalPages
        ];

    }


    pages.forEach(page => {


        if (page === "...") {


            const span =
                document.createElement("span");


            span.textContent = "...";


            pagination.appendChild(span);


            return;

        }


        addPageButton(
            page,
            page,
            true,
            pagination,
            data.page
        );


    });


    addPageButton(
        "Вперёд →",
        data.page + 1,
        data.page < totalPages,
        pagination,
        data.page
    );


}


function addPageButton(
    text,
    page,
    enabled,
    container,
    current
) {


    const button =
        document.createElement("button");


    button.textContent = text;


    if (page === current) {

        button.classList.add(
            "active-page"
        );

    }


    button.disabled =
        !enabled;


    if (enabled) {


        button.onclick = () => {

            loadFiles(page);

        };


    }


    container.appendChild(button);

}


// =======================
// Дата
// =======================

function formatDate(date) {


    return new Date(date)
        .toLocaleString(
            "ru-RU"
        );

}


// старт

loadFiles();