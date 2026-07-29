const content =
    document.getElementById("download-content");


const startButtonId = "start-download";


let timer = null;


document.addEventListener(
    "DOMContentLoaded",
    () => {

        loadStatus();

    }
);


async function loadStatus() {


    const response =
        await fetch("/api/sync");


    const data =
        await response.json();


    renderStatus(data);


    if (
        data.status === "running" ||
        data.status === "queued"
    ) {

        startWatcher();

    }

}


function startWatcher() {


    if (timer) {
        return;
    }


    timer = setInterval(
        loadStatus,
        1000
    );

}


function renderStatus(data) {


    if (
        data &&
        data.status
    ) {


        if (data.status === "running") {


            content.innerHTML = `

                <div class="download-icon">
                    ⏳
                </div>



                <div id="download-status">

                    <p>
                        Время старта:
                        ${formatDate(data.started_at)}
                        (НСК)
                    </p>


                    <p>
                        Получено названий файлов:
                        ${data.total}
                    </p>


                    <p>
                        Скачано:
                        ${data.downloaded}
                        из
                        ${data.total}
                    </p>


                </div>

            `;


            return;

        }


        if (data.status === "completed") {


            content.innerHTML = `

                <div class="download-icon">
                    ✅
                </div>


                <h2>
                    Все файлы уже загружены
                </h2>

            `;


            stopWatcher();

            return;

        }


        if (data.status === "failed") {


            content.innerHTML = `

                <div class="download-icon">
                    ❌
                </div>


                <h2>
                    Ошибка загрузки
                </h2>

            `;


            stopWatcher();

            return;

        }


    }


    content.innerHTML = `

        <div class="download-icon">
            ⬇️
        </div>


        <h2>
            Доступна загрузка файлов
        </h2>


        <button
            id="${startButtonId}"
            class="primary-button"
        >
            Начать загрузку
        </button>

    `;


    document
        .getElementById(startButtonId)
        .addEventListener(
            "click",
            startDownload
        );

}


async function startDownload() {


    const button =
        document.getElementById(startButtonId);


    button.disabled = true;


    await fetch(
        "/api/sync",
        {
            method: "POST"
        }
    );


    loadStatus();

}


function stopWatcher() {


    if (timer) {

        clearInterval(timer);
        timer = null;

    }

}


function formatDate(date) {


    if (!date) {
        return "-";
    }


    return new Date(date)
        .toLocaleString(
            "ru-RU",
            {
                timeZone: "Asia/Novosibirsk"
            }
        );

}