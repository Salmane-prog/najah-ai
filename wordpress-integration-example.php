<?php
/**
 * Plugin Name: Najah AI Integration
 * Description: Intégration partielle de Najah AI avec WordPress
 * Version: 1.0.0
 */

// Empêcher l'accès direct
if (!defined('ABSPATH')) {
    exit;
}

class NajahAIIntegration {
    
    private $api_url = 'https://your-najah-ai-backend.com/api/v1';
    
    public function __construct() {
        add_action('wp_enqueue_scripts', array($this, 'enqueue_scripts'));
        add_shortcode('najah_ai_dashboard', array($this, 'render_dashboard'));
        add_action('wp_ajax_najah_ai_data', array($this, 'ajax_get_data'));
        add_action('wp_ajax_nopriv_najah_ai_data', array($this, 'ajax_get_data'));
    }
    
    public function enqueue_scripts() {
        wp_enqueue_script('najah-ai', plugin_dir_url(__FILE__) . 'assets/najah-ai.js', array('jquery'), '1.0.0', true);
        wp_enqueue_style('najah-ai', plugin_dir_url(__FILE__) . 'assets/najah-ai.css', array(), '1.0.0');
        
        wp_localize_script('najah-ai', 'najahAI', array(
            'ajax_url' => admin_url('admin-ajax.php'),
            'api_url' => $this->api_url,
            'nonce' => wp_create_nonce('najah_ai_nonce')
        ));
    }
    
    public function render_dashboard($atts) {
        $atts = shortcode_atts(array(
            'user_id' => get_current_user_id(),
            'type' => 'student'
        ), $atts);
        
        ob_start();
        ?>
        <div id="najah-ai-dashboard" data-user-id="<?php echo esc_attr($atts['user_id']); ?>" data-type="<?php echo esc_attr($atts['type']); ?>">
            <div class="loading">Chargement des données...</div>
        </div>
        <?php
        return ob_get_clean();
    }
    
    public function ajax_get_data() {
        check_ajax_referer('najah_ai_nonce', 'nonce');
        
        $user_id = intval($_POST['user_id']);
        $type = sanitize_text_field($_POST['type']);
        
        // Appel à votre API Najah AI
        $response = wp_remote_get($this->api_url . '/analytics/student-performances', array(
            'headers' => array(
                'Authorization' => 'Bearer ' . $this->get_user_token($user_id)
            )
        ));
        
        if (is_wp_error($response)) {
            wp_send_json_error('Erreur de connexion à l\'API');
        }
        
        $data = json_decode(wp_remote_retrieve_body($response), true);
        wp_send_json_success($data);
    }
    
    private function get_user_token($user_id) {
        // Logique pour récupérer le token JWT de l'utilisateur
        return get_user_meta($user_id, 'najah_ai_token', true);
    }
}

new NajahAIIntegration();







