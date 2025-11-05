<?php
/**
 * Plugin Name: Review Genius
 * Plugin URI: https://github.com/fyrepaul/review-genius
 * Description: Review management and GBP optimization integration
 * Version: 1.0.0
 * Author: Your Name
 * License: GPL v2 or later
 * Text Domain: review-genius
 */

if ( ! defined('ABSPATH') ) exit;

// Load GBP Optimizer integration
require_once __DIR__ . '/includes/class-rg-gbp-client.php';
require_once __DIR__ . '/includes/class-rg-gbp-settings.php';
require_once __DIR__ . '/includes/class-rg-gbp-admin.php';

add_action('plugins_loaded', function () {
  // Init global settings page
  RG_GBP_Settings::init();

  // Init admin UI for Locations
  RG_GBP_Admin::init();
});

