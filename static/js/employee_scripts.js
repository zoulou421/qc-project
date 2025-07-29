odoo.define('qcproject.employee_scripts', function (require) {
    "use strict";

    var core = require('web.core');

    core.action_registry.add('qcproject_employee_scripts', function () {
        // Form Input Animation
        $('.qcproject-employee-form .form-control').on('focus', function () {
            $(this).addClass('animate__animated animate__tada');
            $(this).on('blur', function () {
                $(this).removeClass('animate__animated animate__tada');
            });
        });

        // Kanban Card Click Animation
        $('.qcproject-kanban-card').on('click', function () {
            $(this).addClass('animate__animated animate__pulse');
            setTimeout(() => {
                $(this).removeClass('animate__animated animate__pulse');
            }, 1000);
        });

        // Notebook Tab Hover Animation
        $('.qcproject-notebook .nav-link').on('mouseenter', function () {
            $(this).addClass('animate__animated animate__bounceIn');
        }).on('mouseleave', function () {
            $(this).removeClass('animate__animated animate__bounceIn');
        });

        // Menu Hover and Click Animation
        $('.o_menu_sections .o_menu_entry').on('mouseenter', function () {
            $(this).addClass('animate__animated animate__pulse');
        }).on('mouseleave', function () {
            $(this).removeClass('animate__animated animate__pulse');
        });

        // Submenu Toggle Animation
        $('.o_menu_sections .dropdown-toggle').on('click', function () {
            var $dropdownMenu = $(this).next('.dropdown-menu');
            if ($dropdownMenu.is(':visible')) {
                $dropdownMenu.removeClass('animate__animated animate__slideInDown');
                $dropdownMenu.addClass('animate__animated animate__slideOutUp');
                setTimeout(() => {
                    $dropdownMenu.removeClass('animate__animated animate__slideOutUp');
                }, 300);
            } else {
                $dropdownMenu.addClass('animate__animated animate__slideInDown');
                setTimeout(() => {
                    $dropdownMenu.removeClass('animate__animated animate__slideInDown');
                }, 300);
            }
        });

        return {};
    });
});