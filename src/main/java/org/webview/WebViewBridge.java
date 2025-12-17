package org.webview;

import android.webkit.WebView;
import android.webkit.WebSettings;
import android.webkit.WebViewClient;
import android.widget.FrameLayout;
import android.content.pm.ActivityInfo;

import org.kivy.android.PythonActivity;

import android.net.Uri;

public class WebViewBridge {

    private static WebView webView;

    /**
     * Mostrar PDF dentro de PDF.js
     */
    public static void showPDF(String pdfPath, boolean isAsset) {
        PythonActivity activity = PythonActivity.mActivity;

        activity.runOnUiThread(() -> {

            activity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_SENSOR);

            if (webView == null) {
                webView = new WebView(activity);

                WebSettings settings = webView.getSettings();
                settings.setJavaScriptEnabled(true);
                settings.setAllowFileAccess(true);
                settings.setAllowContentAccess(true);
                settings.setAllowFileAccessFromFileURLs(true);
                settings.setAllowUniversalAccessFromFileURLs(true);

                webView.setWebViewClient(new WebViewClient());

                // ❗ Interceptar botón BACK dentro del WebView
                webView.setOnKeyListener((v, keyCode, event) -> {
                    if (keyCode == android.view.KeyEvent.KEYCODE_BACK && event.getAction() == android.view.KeyEvent.ACTION_UP) {
                        if (webView.canGoBack()) {
                            webView.goBack();
                        } else {
                            hidePDF();
                        }
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

            String viewer = "file:///android_asset/pdfjs/web/viewer.html";
            String url;

            if (isAsset) {
                // PDF interno (snake)
                url = viewer + "?file=/android_asset/pdfjs/web/" + pdfPath;
            } else {
                // PDF del usuario
                url = viewer + "?file=file://" + pdfPath;
            }

            webView.loadUrl(url);
            webView.setVisibility(WebView.VISIBLE);
            webView.requestFocus(); // necesario para recibir BACK
        });
    }

    /**
     * Cerrar visor PDF y restaurar orientación
     */
    public static void hidePDF() {
        PythonActivity activity = PythonActivity.mActivity;

        activity.runOnUiThread(() -> {
            if (webView != null)
                webView.setVisibility(WebView.GONE);

            activity.setRequestedOrientation(ActivityInfo.SCREEN_ORIENTATION_PORTRAIT);
            activity.getWindow().getDecorView().requestLayout();
        });
    }
}
