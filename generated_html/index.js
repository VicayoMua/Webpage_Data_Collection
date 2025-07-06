document.addEventListener('DOMContentLoaded', () => {
    const searchContainer = document.getElementById('search-container');
    if (!searchContainer) {
        alert(`Failed to find "<div class="page-board" id="search-container"></div>".`);
        return;
    }
    // Create <startLabel> and <startInput>
    const startLabel = document.createElement('label');
    startLabel.htmlFor = 'search-container-start-date-input';
    startLabel.id = 'search-container-start-date-input-label';
    startLabel.textContent = '开始日期：';
    const startInput = document.createElement('input');
    startInput.type = 'date';
    startInput.id = 'search-container-start-date-input';
    // Create <endLabel> and <endInput>
    const endLabel = document.createElement('label');
    endLabel.htmlFor = 'search-container-end-date-input';
    endLabel.id = 'search-container-end-date-input-label';
    endLabel.textContent = '结束日期：';
    const endInput = document.createElement('input');
    endInput.type = 'date';
    endInput.id = 'search-container-end-date-input';
    // append <startLabel>, <startInput>, <endLabel>, and <endInput> to <searchContainer>
    searchContainer.append(startLabel, startInput, endLabel, endInput);
    // listen to any changes on <startInput> and <endInput>
    const pageBoardItems = document.querySelectorAll('div.page-board-item');
    startInput.addEventListener('change', filterByDate);
    endInput.addEventListener('change', filterByDate);

    // Filter items by selected date range
    function filterByDate() {
        const startDate = startInput.value ? new Date(startInput.value) : null;
        const endDate = endInput.value ? new Date(endInput.value) : null;
        pageBoardItems.forEach((pageBoardItem) => {
            const span = pageBoardItem.querySelector('span');
            if (span === null || span.textContent.trim() === '') { // no date span → hide
                pageBoardItem.style.display = 'none'; // hide
                return;
            }
            const date = parseDateString(span.textContent.trim());
            if (date === null) { // failed to parse date string → show
                alert(`Failed to parse date string "${span.textContent.trim()}".`);
                pageBoardItem.style.display = 'block'; // show
                return;
            }
            if ((startDate !== null && date < startDate) || (endDate !== null && date > endDate)) {
                pageBoardItem.style.display = 'none'; // hide
                return;
            }
            pageBoardItem.style.display = 'block'; // show

            function parseDateString(str) {
                for (const reg of [
                    /^(\d{4})年(\d{1,2})月(\d{1,2})日$/,  // Chinese format: "2025年6月23日"
                    /^(\d{4})-(\d{1,2})-(\d{1,2})$/,     // English format 1: "2025-06-23"
                    /^(\d{4})\/(\d{1,2})\/(\d{1,2})$/,   // English format 2: "2025/06/23"
                    /^(\d{4})\.(\d{1,2})\.(\d{1,2})$/,   // English format 3: "2025.06.23"
                ]) {
                    const m = str.match(reg);
                    if (m !== null) {
                        const [_, yr, mon, day] = m;
                        return new Date(`${yr}-${mon}-${day}`);
                    }
                }
                return null;
            }
        });
    }

});

// grab one or all
// const items = document.querySelectorAll('.page-board-item');
//
// // hide every item
// items.forEach(el => el.style.display = 'none');
//
// // show them again
// items.forEach(el => el.style.display = 'block');