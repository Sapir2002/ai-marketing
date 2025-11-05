<?php
if ( ! defined('ABSPATH') ) exit;

class RG_GBP_Client {

  protected static function base() {
    return untrailingslashit( get_option('rg_gbp_api_base', '') );
  }

  public static function fetch_reviews($location_id) {
    $base = self::base();
    if (!$base) return new WP_Error('no_base', 'API base URL not set.');
    $url  = $base . '/gbp/reviews?location_id=' . urlencode($location_id);
    $res  = wp_remote_get($url, ['timeout' => 20]);
    if (is_wp_error($res)) return $res;
    return json_decode(wp_remote_retrieve_body($res), true);
  }

  public static function apply_reply($review_id, $payload = []) {
    $base = self::base();
    if (!$base) return new WP_Error('no_base', 'API base URL not set.');
    $url  = $base . '/gbp/reviews/apply';
    $res  = wp_remote_post($url, [
      'timeout' => 20,
      'headers' => ['Content-Type' => 'application/json'],
      'body'    => wp_json_encode(array_merge(['id' => $review_id], $payload)),
    ]);
    if (is_wp_error($res)) return $res;
    return json_decode(wp_remote_retrieve_body($res), true);
  }

  public static function schedule_posts($location_id, $freq, $topics=[]) {
    $base = self::base();
    if (!$base) return new WP_Error('no_base', 'API base URL not set.');
    $url  = $base . '/gbp/posting/schedule';
    $res  = wp_remote_post($url, [
      'timeout' => 20,
      'headers' => ['Content-Type' => 'application/json'],
      'body'    => wp_json_encode(compact('location_id','freq','topics')),
    ]);
    if (is_wp_error($res)) return $res;
    return json_decode(wp_remote_retrieve_body($res), true);
  }

  public static function optimize($location_id, $fields=[]) {
    $base = self::base();
    if (!$base) return new WP_Error('no_base', 'API base URL not set.');
    $url  = $base . '/gbp/optimize';
    $res  = wp_remote_post($url, [
      'timeout' => 20,
      'headers' => ['Content-Type' => 'application/json'],
      'body'    => wp_json_encode(compact('location_id','fields')),
    ]);
    if (is_wp_error($res)) return $res;
    return json_decode(wp_remote_retrieve_body($res), true);
  }
}

