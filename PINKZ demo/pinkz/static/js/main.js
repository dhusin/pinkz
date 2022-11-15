
(function ($) {
    "use strict";

    /*[ Load page ]
    ===========================================================*/
    $(".animsition").animsition({
        inClass: 'fade-in',
        outClass: 'fade-out',
        inDuration: 1500,
        outDuration: 800,
        linkElement: '.animsition-link',
        loading: true,
        loadingParentElement: 'html',
        loadingClass: 'animsition-loading-1',
        loadingInner: '<div class="loader05"></div>',
        timeout: false,
        timeoutCountdown: 5000,
        onLoadEvent: true,
        browser: [ 'animation-duration', '-webkit-animation-duration'],
        overlay : false,
        overlayClass : 'animsition-overlay-slide',
        overlayParentElement : 'html',
        transition: function(url){ window.location.href = url; }
    });
    
    /*[ Back to top ]
    ===========================================================*/
    var windowH = $(window).height()/2;

    $(window).on('scroll',function(){
        if ($(this).scrollTop() > windowH) {
            $("#myBtn").css('display','flex');
        } else {
            $("#myBtn").css('display','none');
        }
    });

    $('#myBtn').on("click", function(){
        $('html, body').animate({scrollTop: 0}, 300);
    });


    /*==================================================================
    [ Fixed Header ]*/
    var headerDesktop = $('.container-menu-desktop');
    var wrapMenu = $('.wrap-menu-desktop');

    if($('.top-bar').length > 0) {
        var posWrapHeader = $('.top-bar').height();
    }
    else {
        var posWrapHeader = 0;
    }
    

    if($(window).scrollTop() > posWrapHeader) {
        $(headerDesktop).addClass('fix-menu-desktop');
        $(wrapMenu).css('top',0); 
    }  
    else {
        $(headerDesktop).removeClass('fix-menu-desktop');
        $(wrapMenu).css('top',posWrapHeader - $(this).scrollTop()); 
    }

    $(window).on('scroll',function(){
        if($(this).scrollTop() > posWrapHeader) {
            $(headerDesktop).addClass('fix-menu-desktop');
            $(wrapMenu).css('top',0); 
        }  
        else {
            $(headerDesktop).removeClass('fix-menu-desktop');
            $(wrapMenu).css('top',posWrapHeader - $(this).scrollTop()); 
        } 
    });


    /*==================================================================
    [ Menu mobile ]*/
    $('.btn-show-menu-mobile').on('click', function(){
        $(this).toggleClass('is-active');
        $('.menu-mobile').slideToggle();
    });

    var arrowMainMenu = $('.arrow-main-menu-m');

    for(var i=0; i<arrowMainMenu.length; i++){
        $(arrowMainMenu[i]).on('click', function(){
            $(this).parent().find('.sub-menu-m').slideToggle();
            $(this).toggleClass('turn-arrow-main-menu-m');
        })
    }

    $(window).resize(function(){
        if($(window).width() >= 992){
            if($('.menu-mobile').css('display') == 'block') {
                $('.menu-mobile').css('display','none');
                $('.btn-show-menu-mobile').toggleClass('is-active');
            }

            $('.sub-menu-m').each(function(){
                if($(this).css('display') == 'block') { console.log('hello');
                    $(this).css('display','none');
                    $(arrowMainMenu).removeClass('turn-arrow-main-menu-m');
                }
            });
                
        }
    });


    /*==================================================================
    [ Show / hide modal search ]*/
    $('.js-show-modal-search').on('click', function(){
        $('.modal-search-header').addClass('show-modal-search');
        $(this).css('opacity','0');
    });

    $('.js-hide-modal-search').on('click', function(){
        $('.modal-search-header').removeClass('show-modal-search');
        $('.js-show-modal-search').css('opacity','1');
    });

    $('.container-search-header').on('click', function(e){
        e.stopPropagation();
    });


    /*==================================================================
    [ Isotope ]*/
    var $topeContainer = $('.isotope-grid');
    var $filter = $('.filter-tope-group');

    // filter items on button click
    $filter.each(function () {
        $filter.on('click', 'button', function () {
            var filterValue = $(this).attr('data-filter');
            $topeContainer.isotope({filter: filterValue});
        });
        
    });

    // init Isotope
    $(window).on('load', function () {
        var $grid = $topeContainer.each(function () {
            $(this).isotope({
                itemSelector: '.isotope-item',
                layoutMode: 'fitRows',
                percentPosition: true,
                animationEngine : 'best-available',
                masonry: {
                    columnWidth: '.isotope-item'
                }
            });
        });
    });

    var isotopeButton = $('.filter-tope-group button');

    $(isotopeButton).each(function(){
        $(this).on('click', function(){
            for(var i=0; i<isotopeButton.length; i++) {
                $(isotopeButton[i]).removeClass('how-active1');
            }

            $(this).addClass('how-active1');
        });
    });

    /*==================================================================
    [ Filter / Search product ]*/
    $('.js-show-filter').on('click',function(){
        $(this).toggleClass('show-filter');
        $('.panel-filter').slideToggle(400);

        if($('.js-show-search').hasClass('show-search')) {
            $('.js-show-search').removeClass('show-search');
            $('.panel-search').slideUp(400);
        }    
    });

    $('.js-show-search').on('click',function(){
        $(this).toggleClass('show-search');
        $('.panel-search').slideToggle(400);

        if($('.js-show-filter').hasClass('show-filter')) {
            $('.js-show-filter').removeClass('show-filter');
            $('.panel-filter').slideUp(400);
        }    
    });




    /*==================================================================
    [ Cart ]*/
    $('.js-show-cart').on('click',function(){
        // ajax call
        var url = "http://127.0.0.1:8000/";
        $.ajax({
            method: "GET",
            url: url+"mini_cart_view",
            success: function(response){
                if (response["products"].length == 0)
                {
                    $(".js-panel-cart").find("#cart_header").html("Your cart is empty")
                } 
                else{
                    let i;
                    $('.js-panel-cart').find(".cart_list").remove()
                    for(i = 0; i < response["products"].length;i++){
                        let prod_name = response["products"][i]["prod_name"];

                        $(".js-panel-cart").find(".cart_mini_display").append(`<li class="header-cart-item flex-w flex-t m-b-12 cart_list">
						<div class="header-cart-item-img">
							<img src="/media/${response["products"][i]["prod_img"]}" alt="IMG">
						</div>

						<div class="header-cart-item-txt p-t-8">
							<a href="#" class="header-cart-item-name m-b-18 hov-cl1 trans-04">
                            ${prod_name}
							</a>

							<span class="header-cart-item-info">
								${response["products"][i]["quantity"]} x ₹${response["products"][i]["price"]}
							</span>
						</div>
					</li>`)
                    }
                }
                $(".js-panel-cart").find(".header-cart-total").html("Total: ₹"+response['total'])
                
            }
                
        });
        $('.js-panel-cart').addClass('show-header-cart');
    });

    $('.js-hide-cart').on('click',function(){
        $('.js-panel-cart').removeClass('show-header-cart');
    });

    /*==================================================================
    [ Cart ]*/
    $('.js-show-sidebar').on('click',function(){
        $('.js-sidebar').addClass('show-sidebar');
    });

    $('.js-hide-sidebar').on('click',function(){
        $('.js-sidebar').removeClass('show-sidebar');
    });

    /*==================================================================
    [ +/- num product ]*/
    $('.btn-num-product-down').on('click', function(){
        var numProduct = Number($(this).next().val());
        if(numProduct > 0) $(this).next().val(numProduct - 1);
        var url = "http://127.0.0.1:8000/";
        var p_id = $(this).attr("p_id")    
        console.log(p_id)
        $.ajax({
            method: "GET",
            url: url+"manage_cart/"+p_id+"?action=dcr",
            success: function(response){
                location. reload()
            }
        });
        
    });

    $('.btn-num-product-up').on('click', function(){
        var numProduct = Number($(this).prev().val());
        $(this).prev().val(numProduct + 1);
        var url = "http://127.0.0.1:8000/";
        var p_id = $(this).attr("p_id") 
        $.ajax({
            method: "GET",
            url: url+"manage_cart/"+p_id+"?action=inc",
            async: true,
            success: function(response){
                location. reload()
            }
        });
        
    });

    /*==================================================================
    [ Rating ]*/
    $('.wrap-rating').each(function(){
        var item = $(this).find('.item-rating');
        var rated = -1;
        var input = $(this).find('input');
        $(input).val(0);

        $(item).on('mouseenter', function(){
            var index = item.index(this);
            var i = 0;
            for(i=0; i<=index; i++) {
                $(item[i]).removeClass('zmdi-star-outline');
                $(item[i]).addClass('zmdi-star');
            }

            for(var j=i; j<item.length; j++) {
                $(item[j]).addClass('zmdi-star-outline');
                $(item[j]).removeClass('zmdi-star');
            }
        });

        $(item).on('click', function(){
            var index = item.index(this);
            rated = index;
            $(input).val(index+1);
        });

        $(this).on('mouseleave', function(){
            var i = 0;
            for(i=0; i<=rated; i++) {
                $(item[i]).removeClass('zmdi-star-outline');
                $(item[i]).addClass('zmdi-star');
            }

            for(var j=i; j<item.length; j++) {
                $(item[j]).addClass('zmdi-star-outline');
                $(item[j]).removeClass('zmdi-star');
            }
        });
    });

    $(".post-comment").on('click',function(e){
        e.preventDefault();
        
        if(String($("#review").val())=="" || $(".dis-none").val()==0){
            $("#review").css("border","2px solid red")
        }
        else{
            $("#review").css("border","1px solid #e6e6e6")
            $.ajax({
                method:"GET",
                data : {
                    "comment": String($("#review").val()),
                    "ratings": $(".dis-none").val(),
                    'id': $(this).attr("data-id")
                },
                url : "http://127.0.0.1:8000/add_comment",
                success : function(response){
                    location.reload()
                }       
            });
    }
    });
    
    /*==================================================================
    [ Show modal1 ]*/
    $('.js-show-modal1').on('click',function(e){
        e.preventDefault();
        var img_url
        var id = $(this).attr("productdesc");
        var url = "http://127.0.0.1:8000/";
        // console.log(id)
        $.ajax({
            method: "GET",
            url: url+'quickViewDetails/'+id,
            success: function(response){
                img_url = response[0].fields.image
                $('.js-modal1').find('.prod_name').html(response[0].fields.productName) 
                $('.js-modal1').find('.prod_price').html(response[0].fields.price) 
                $('.js-modal1').find('.prod_desc').html(response[0].fields.productDesc) 
                $('.js-modal1').find('.prod_img').attr('src',"/media/"+img_url)
                $('.js-modal1').find('.thubnail').attr('data-thumb',"/media/"+img_url)
                $('.js-modal1').find('.expand').attr('href',"/media/"+img_url)
                $('.js-modal1').find('.cartbutton').attr('data-id',id)
                $('.js-modal1').find('.heartbutton').attr('data-id',id)
            }
                
        });
        
        $('.js-modal1').addClass('show-modal1');
        
    });

    $('.js-hide-modal1').on('click',function(){
        $('.js-modal1').removeClass('show-modal1');
    });



})(jQuery);