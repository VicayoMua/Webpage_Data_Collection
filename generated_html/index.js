document.addEventListener('DOMContentLoaded', () => {
    const searchContainer = document.getElementById('search-container');
    if (!searchContainer) {
        alert(`Cannot find "<div class="page-board" id="search-container"></div>".`);
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