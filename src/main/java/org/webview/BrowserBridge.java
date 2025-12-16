package org.webview;

import android.webkit.WebView;
import android.webkit.WebSettings;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.content.pm.ActivityInfo;
import android.view.KeyEvent;

import org.kivy.android.PythonActivity;

public class BrowserBridge {

    private static WebView webView;

    public static void showWeb(String url) {
        PythonActivity activity = PythonActivity.mActivity;

        activity.runOnUiThread(() -> {

            activity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_SENSOR);

            if (webView == null) {
                webView = new WebView(activity);

                WebSettings webSettings = webView.getSettings();
                webSettings.setJavaScriptEnabled(true);

                webView.setWebViewClient(new WebViewClient());

                // ❗ Interceptar botón BACK dentro del WebView
                webView.setOnKeyListener((v, keyCode, event) -> {
                    if (keyCode == KeyEvent.KEYCODE_BACK && event.getAction() == KeyEvent.ACTION_UP) {

                        // Si hay historial, retrocede
                        if (webView.canGoBack()) {
                            webView.goBack();
                            return true;
                        }

                        // Si no hay historial, cerrar el WebView
                        hideWeb();
                        return true; // Consumimos BACK
                    }
                    return false;
                });

                FrameLayout.LayoutParams params =
                        new FrameLayout.LayoutParams(
                                FrameLayout.LayoutParams.MATCH_PARENT,
                                FrameLayout.LayoutParams.MATCH_PARENT
                        );

                activity.addContentView(webView, params);
            }

            webView.loadUrl(url);
            webView.setVisibility(WebView.VISIBLE);
            webView.requestFocus();
        });
    }

    public static void hideWeb() {
        PythonActivity activity = PythonActivity.mActivity;

        activity.runOnUiThread(() -> {
            if (webView != null)
                webView.setVisibility(WebView.GONE);

            activity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
            activity.getWindow().getDecorView().requestLayout();
        });
    }
}

