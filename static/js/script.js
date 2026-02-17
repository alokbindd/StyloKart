// some scripts

// jquery ready start
$(document).ready(function() {
	// jQuery code


    /* ///////////////////////////////////////

    THESE FOLLOWING SCRIPTS ONLY FOR BASIC USAGE, 
    For sliders, interactions and other

    */ ///////////////////////////////////////
    

	//////////////////////// Prevent closing from click inside dropdown
    $(document).on('click', '.dropdown-menu', function (e) {
      e.stopPropagation();
    });


    $('.js-check :radio').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $('input[name='+ check_attr_name +']').closest('.js-check').removeClass('active');
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');

        } else {
            item.removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });


    $('.js-check :checkbox').change(function () {
        var check_attr_name = $(this).attr('name');
        if ($(this).is(':checked')) {
            $(this).closest('.js-check').addClass('active');
           // item.find('.radio').find('span').text('Add');
        } else {
            $(this).closest('.js-check').removeClass('active');
            // item.find('.radio').find('span').text('Unselect');
        }
    });



	//////////////////////// Bootstrap tooltip
	if($('[data-toggle="tooltip"]').length>0) {  // check if element exists
		$('[data-toggle="tooltip"]').tooltip()
	} // end if
    
    //////////////////////// Home hero carousel (banners)
    (function initHeroCarousel() {
        var dataEl = document.getElementById('hero-banners-data');
        var hero = document.getElementById('heroCarousel');
        if (!dataEl || !hero) return;

        var banners;
        try {
            banners = JSON.parse(dataEl.textContent || '[]');
        } catch (e) {
            banners = [];
        }
        if (!Array.isArray(banners) || banners.length === 0) return;

        var idx = 0;
        var titleEl = document.getElementById('heroTitle');
        var subtitleEl = document.getElementById('heroSubtitle');
        var ctaEl = document.getElementById('heroCta');
        var prevBtn = hero.querySelector('.hero-carousel-btn--prev');
        var nextBtn = hero.querySelector('.hero-carousel-btn--next');
        var defaultCtaHref = (ctaEl && ctaEl.getAttribute('href')) ? ctaEl.getAttribute('href') : '/';

        function setBanner(i) {
            var b = banners[i];
            if (!b) return;

            if (b.image_url) {
                hero.style.backgroundImage = "url('" + String(b.image_url).replace(/'/g, "\\'") + "')";
            }

            if (titleEl) titleEl.textContent = b.title || '';

            if (subtitleEl) {
                var sub = b.subtitle || '';
                subtitleEl.textContent = sub;
                subtitleEl.style.display = sub ? '' : 'none';
            }

            if (ctaEl) {
                ctaEl.textContent = b.button_text || ctaEl.textContent || 'Shop Now';
                ctaEl.setAttribute('href', b.button_link || defaultCtaHref);
            }
        }

        function next() {
            idx = (idx + 1) % banners.length;
            setBanner(idx);
        }

        function prev() {
            idx = (idx - 1 + banners.length) % banners.length;
            setBanner(idx);
        }

        if (nextBtn) nextBtn.addEventListener('click', next);
        if (prevBtn) prevBtn.addEventListener('click', prev);

        hero.addEventListener('keydown', function (e) {
            if (e.key === 'ArrowLeft') {
                e.preventDefault();
                prev();
            }
            if (e.key === 'ArrowRight') {
                e.preventDefault();
                next();
            }
        });

        setBanner(idx);
    })();

}); 
// jquery end

setTimeout(function(){
    $('#message').fadeOut('slow')
}, 2000)

function printInvoice() {
    window.print();
} 