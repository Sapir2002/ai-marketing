<?php
if ( ! defined('ABSPATH') ) exit;

/**
 * Assumes a Location CPT exists. If the CPT key differs, set CPT_SLUG accordingly.
 */
class RG_GBP_Admin {

  const CPT_SLUG = 'location'; // change if your CPT key is different

  // meta keys
  const META_LOCATION_ID   = '_gbp_location_id';
  const META_AUTO_REPLY    = '_gbp_auto_reply_enabled';
  const META_REPLY_PROMPT  = '_gbp_reply_prompt';
  const META_BAD_NOTIFY    = '_gbp_bad_review_notify';
  const META_POST_FREQ     = '_gbp_post_freq';
  const META_POST_TOPICS   = '_gbp_post_topics';
  const META_OPT_DESC      = '_gbp_opt_description';
  const META_OPT_QA        = '_gbp_opt_qa';
  const META_OPT_SOCIAL    = '_gbp_opt_social';

  public static function init() {
    add_action('add_meta_boxes', [__CLASS__, 'add_box']);
    add_action('save_post_' . self::CPT_SLUG, [__CLASS__, 'save'], 10, 2);
    add_action('admin_post_rg_gbp_fetch_reviews', [__CLASS__, 'handle_fetch_reviews']);
    add_action('admin_post_rg_gbp_send_sample',   [__CLASS__, 'handle_send_sample']);
    add_action('admin_notices', [__CLASS__, 'show_admin_notices']);
  }

  public static function add_box() {
    add_meta_box(
      'rg_gbp_box',
      'GBP Optimizer',
      [__CLASS__, 'render_box'],
      self::CPT_SLUG,
      'normal',
      'default'
    );
  }

  public static function render_box($post) {
    wp_nonce_field('rg_gbp_save', 'rg_gbp_nonce');
    $g = function($k,$d=''){ return get_post_meta($post->ID,$k,true) ?: $d; };

    $loc_id   = esc_attr($g(self::META_LOCATION_ID));
    $auto     = (bool)$g(self::META_AUTO_REPLY,false);
    $prompt   = esc_textarea($g(self::META_REPLY_PROMPT));
    $bad      = (bool)$g(self::META_BAD_NOTIFY,false);
    $freq     = esc_attr($g(self::META_POST_FREQ,'weekly'));
    $topics   = esc_attr($g(self::META_POST_TOPICS,''));
    $optDesc  = (bool)$g(self::META_OPT_DESC,false);
    $optQA    = (bool)$g(self::META_OPT_QA,false);
    $optSoc   = (bool)$g(self::META_OPT_SOCIAL,false);

    $fetch_url = wp_nonce_url(admin_url('admin-post.php?action=rg_gbp_fetch_reviews&post_id='.$post->ID), 'rg_gbp_fetch');
    $send_url  = wp_nonce_url(admin_url('admin-post.php?action=rg_gbp_send_sample&post_id='.$post->ID), 'rg_gbp_send');

    echo '<table class="form-table">';
    echo '<tr><th>Location ID</th><td><input type="text" name="rg_gbp_location_id" value="'.$loc_id.'" class="regular-text" placeholder="Google Business Location ID"></td></tr>';

    echo '<tr><th>Auto-reply to Reviews</th><td>';
    echo '<label><input type="checkbox" name="rg_gbp_auto_reply" '.checked($auto,true,false).'> Enable</label><br>';
    echo '<label>Reply Prompt<br><textarea name="rg_gbp_reply_prompt" class="large-text" rows="4">'.$prompt.'</textarea></label><br>';
    echo '<label><input type="checkbox" name="rg_gbp_bad_notify" '.checked($bad,true,false).'> Notify on bad reviews</label>';
    echo '</td></tr>';

    echo '<tr><th>GBP Posting</th><td>';
    echo '<label>Frequency ';
    echo '<select name="rg_gbp_post_freq">';
    foreach (['daily','weekly','custom'] as $f) {
      echo '<option value="'.$f.'" '.selected($freq,$f,false).'>'.ucfirst($f).'</option>';
    }
    echo '</select></label><br>';
    echo '<label>Topics (comma-separated) <input type="text" name="rg_gbp_post_topics" value="'.$topics.'" class="regular-text"></label>';
    echo '</td></tr>';

    echo '<tr><th>Optimize Fields</th><td>';
    echo '<label><input type="checkbox" name="rg_gbp_opt_description" '.checked($optDesc,true,false).'> Description</label><br>';
    echo '<label><input type="checkbox" name="rg_gbp_opt_qa" '.checked($optQA,true,false).'> Q&A</label><br>';
    echo '<label><input type="checkbox" name="rg_gbp_opt_social" '.checked($optSoc,true,false).'> Social links</label>';
    echo '</td></tr>';

    echo '<tr><th>Test Actions</th><td>';
    echo '<a href="'.esc_url($fetch_url).'" class="button">Fetch Reviews</a> ';
    echo '<a href="'.esc_url($send_url).'" class="button button-primary">Send Sample Reply</a>';
    echo '</td></tr>';

    echo '</table>';
  }

  public static function save($post_id, $post) {
    if (!isset($_POST['rg_gbp_nonce']) || !wp_verify_nonce($_POST['rg_gbp_nonce'],'rg_gbp_save')) return;
    if (defined('DOING_AUTOSAVE') && DOING_AUTOSAVE) return;
    if (!current_user_can('edit_post', $post_id)) return;

    $cb = function($key){ return isset($_POST[$key]) ? '1' : ''; };

    update_post_meta($post_id, self::META_LOCATION_ID, sanitize_text_field($_POST['rg_gbp_location_id'] ?? ''));
    update_post_meta($post_id, self::META_AUTO_REPLY, $cb('rg_gbp_auto_reply'));
    update_post_meta($post_id, self::META_REPLY_PROMPT, wp_kses_post($_POST['rg_gbp_reply_prompt'] ?? ''));
    update_post_meta($post_id, self::META_BAD_NOTIFY, $cb('rg_gbp_bad_notify'));
    update_post_meta($post_id, self::META_POST_FREQ, sanitize_text_field($_POST['rg_gbp_post_freq'] ?? 'weekly'));
    update_post_meta($post_id, self::META_POST_TOPICS, sanitize_text_field($_POST['rg_gbp_post_topics'] ?? ''));
    update_post_meta($post_id, self::META_OPT_DESC, $cb('rg_gbp_opt_description'));
    update_post_meta($post_id, self::META_OPT_QA, $cb('rg_gbp_opt_qa'));
    update_post_meta($post_id, self::META_OPT_SOCIAL, $cb('rg_gbp_opt_social'));
  }

  public static function handle_fetch_reviews() {
    if (!current_user_can('edit_posts')) wp_die('No permission.');
    check_admin_referer('rg_gbp_fetch');
    $post_id = absint($_GET['post_id'] ?? 0);
    $loc_id  = get_post_meta($post_id, self::META_LOCATION_ID, true);
    if (empty($loc_id)) {
      self::admin_notice_from_result(new WP_Error('no_location', 'Location ID not set.'), '');
      return;
    }
    $res = RG_GBP_Client::fetch_reviews($loc_id);
    self::admin_notice_from_result($res, 'Fetched reviews');
  }

  public static function handle_send_sample() {
    if (!current_user_can('edit_posts')) wp_die('No permission.');
    check_admin_referer('rg_gbp_send');
    $post_id = absint($_GET['post_id'] ?? 0);
    // In a real flow you'd choose a review_id from fetched data:
    $res = RG_GBP_Client::apply_reply('sample-review-id', [
      'action'  => 'approve',
      'note'    => 'Test from Review Genius admin',
    ]);
    self::admin_notice_from_result($res, 'Sent sample reply');
  }

  protected static function admin_notice_from_result($res, $ok_msg) {
    if (is_wp_error($res)) {
      $msg = urlencode($res->get_error_message());
      wp_safe_redirect( add_query_arg('rg_gbp_msg', "ERROR: $msg", wp_get_referer()) );
    } else {
      $msg = urlencode($ok_msg);
      wp_safe_redirect( add_query_arg('rg_gbp_msg', "OK: $msg", wp_get_referer()) );
    }
    exit;
  }

  public static function show_admin_notices() {
    if (!isset($_GET['rg_gbp_msg'])) return;
    $msg = sanitize_text_field($_GET['rg_gbp_msg']);
    if (strpos($msg, 'ERROR:') === 0) {
      echo '<div class="notice notice-error is-dismissible"><p>' . esc_html($msg) . '</p></div>';
    } else {
      echo '<div class="notice notice-success is-dismissible"><p>' . esc_html($msg) . '</p></div>';
    }
  }
}

