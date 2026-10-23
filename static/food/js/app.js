// Behaviour shared by the food pages (index.html and order.html).
// The order page has no category filter and no mobile menu, so every block
// first checks that its elements exist (?.) instead of crashing.

// Opens / closes the cart popup. The templates call it with onclick="modal()",
// so it has to stay a global function.
function modal() {
    document.querySelector('.modal')?.classList.toggle('modalShow');
}

(function () {
    // 1. Burger button in the header
    const burger = document.querySelector('button.main span');
    burger?.addEventListener('click', () => {
        burger.classList.toggle('show');
        document.querySelector('.main__menu')?.classList.toggle('show');
        document.querySelector('button.main')?.classList.toggle('show');
    });

    // 2. Category filter: "Barchasi" (all), Pitsa, Kombo, ...
    const filterButtons = document.querySelectorAll('.filter button');
    const rows = document.querySelectorAll('.slide .row');
    const titles = document.querySelectorAll('.slide .big__title');
    const slideButtons = document.querySelectorAll('.slide__btn');

    // Show the elements that belong to `category` (or all of them) and hide the rest.
    function showOnly(elements, category, display) {
        elements.forEach((element) => {
            const visible = category === 'all' || element.classList.contains(category);
            element.style.display = visible ? display : 'none';
        });
    }

    filterButtons.forEach((button) => {
        button.addEventListener('click', () => {
            document.querySelector('.filter button.active')?.classList.remove('active');
            button.classList.add('active');

            const category = button.dataset.id;
            showOnly(rows, category, 'flex');
            showOnly(titles, category, 'block');
            if (window.innerWidth <= 766) {
                showOnly(slideButtons, category, 'block');
            }
        });
    });

    // 3. Mobile: the button under a category opens / closes its product row
    slideButtons.forEach((button) => {
        button.addEventListener('click', () => {
            rows.forEach((row) => {
                if (row.classList.contains(button.dataset.id)) {
                    row.classList.toggle('open');
                }
            });
        });
    });

    // 4. Mobile footer: each button opens the list next to it
    [
        ['.mob__menu--btn:not(.add)', 'ul.point'],
        ['.mob__menu--btn.add', 'ul.addition'],
    ].forEach(([buttonSelector, listSelector]) => {
        document.querySelector(buttonSelector)?.addEventListener('click', () => {
            document.querySelector(listSelector)?.classList.toggle('ulList');
        });
    });
})();
