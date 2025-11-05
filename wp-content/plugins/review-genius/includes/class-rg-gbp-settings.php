<?php
if ( ! defined('ABSPATH') ) exit;

class RG_GBP_Settings {
  const OPTION_API_BASE = 'rg_gbp_api_base';

  public static function init() {
    add_action('admin_menu', [__CLASS__, 'add_menu']);
    add_action('admin_init', [__CLASS__, 'register']);
  }

  public static function add_menu() {
    add_options_page(
      'Review Genius – GBP',
      'Review Genius – GBP',
      'manage_options',
      'rg-gbp-settings',
      [__CLASS__, 'render']
    );
  }

  public static function register() {
    register_setting('rg_gbp_group', self::OPTION_API_BASE, [
      'type' => 'string',
      'sanitize_callback' => function($url) {
        $url = trim($url);
        if ($url && ! filter_var($url, FILTER_VALIDATE_URL)) {
          add_settings_error(self::OPTION_API_BASE, 'invalid_url', 'API Base URL must be a valid URL.');
          return get_option(self::OPTION_API_BASE, '');
        }
        return untrailingslashit($url);
      },
      'default' => ''
    ]);

    add_settings_section('rg_gbp_main', 'GBP Optimizer', '__return_false', 'rg-gbp-settings');

    add_settings_field(
      self::OPTION_API_BASE,
      'Backend API Base URL',
      function() {
        $val = esc_attr(get_option(RG_GBP_Settings::OPTION_API_BASE, ''));
        echo '<input type="url" name="'.RG_GBP_Settings::OPTION_API_BASE.'" value="'.$val.'" class="regular-text" placeholder="https://optimizer.example.com">';
        echo '<p class="description">Base URL for the gbp-optimizer server.</p>';
      },
      'rg-gbp-settings',
      'rg_gbp_main'
    );
  }

  public static function render() {
    if (!current_user_can('manage_options')) return;
    echo '<div class="wrap"><h1>Review Genius – GBP Settings</h1>';
    echo '<form method="post" action="options.php">';
    settings_fields('rg_gbp_group');
    do_settings_sections('rg-gbp-settings');
    submit_button('Save Settings');
    echo '</form></div>';
  }
}

