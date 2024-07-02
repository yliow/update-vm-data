;; load newer bytecode if exists for packages
(setq load-prefer-newer t)

;; save backup files (*~) and places at ~/.emacs.d/ instead
(setq save-place-file (concat user-emacs-directory "places")
      backup-directory-alist `(("." . ,(concat user-emacs-directory
                                               "backups"))))

;; when using middle mouse to yank, yank at point instead of click location
(setq mouse-yank-at-point t)

;; instead of an audible alarm, show a visual cue
(setq visible-bell t)


;; blank line at end-of-file
(setq require-final-newline t)

;;-----------------------------------------------------------------------------
;; Keybinds Replacemenet for some default keybinds with powered-up versions
;;-----------------------------------------------------------------------------

;; interactive buffer over default buffer
(global-set-key (kbd "C-x C-b") 'ibuffer)

;; favor regex searches over regular, swap the keybinds
(global-set-key (kbd "C-s") 'isearch-forward-regexp)
(global-set-key (kbd "C-r") 'isearch-backward-regexp)
(global-set-key (kbd "C-M-s") 'isearch-forward)
(global-set-key (kbd "C-M-r") 'isearch-backward)

;;-----------------------------------------------------------------------------
;; Look and feel
;;-----------------------------------------------------------------------------

;; Disable the startup message
(setq inhibit-startup-screen t)

;; Disable menu, scroll and tool bars
(menu-bar-mode 1)
(when (fboundp 'tool-bar-mode)
  (tool-bar-mode -1))
(when (fboundp 'scroll-bar-mode)
  (scroll-bar-mode -1))

;; Line and column numbers on.
(line-number-mode 1)
(column-number-mode 1)

;; Line fill set to 79
(setq-default fill-column 79)

;; Highlight matching parens
(show-paren-mode 1)

;; Tab width set to 4
(setq tab-width 4)

;; No tabs for indentation
(setq-default indent-tabs-mode nil)

;; Automatically indent after a newline (like vi)
(global-set-key (kbd "RET") 'newline-and-indent)

;; Save position when buffers are closed
(setq-default save-place t)

(setenv "DICTIONARY" "en_US")

;; C-style modes
;; -------------
;; C mode is nice, but I have a particular style that I like.  This tries
;; to be a bit smarter about automatically inserting newlines around braces
;; for enums and single- and multi-line initializer lists.  It also sets up
;; highlighting for Doxygen style comments.
;;
(defun c-brace-open (syntax pos)
  (save-excursion
    (let ((start (c-point 'bol))
          langelem)
      (if (and (eq syntax 'brace-list-open)
               (setq langelem (assq 'brace-list-open c-syntactic-context))
               (progn (goto-char (c-langelem-pos langelem))
                      (if (eq (char-after) ?{)
                          (c-safe (c-forward-sexp -1)))
                      (looking-at "\\<enum\\>[^_]")))
          '(before after)
        (if (< (point) start)
            '(after))))))
(defun c-brace-close (syntax pos)
  (save-excursion
    (goto-char pos)
    (if (> (c-point 'bol)
           (progn (up-list -1) (point)))
        '(before))))
(defconst doxygen-font-lock-doc-comments
  `(("\\s-\\([\\@].*?\\)\\s-"
     1 font-lock-constant-face prepend nil)                     ; ,c-doc-markup-face-name
    ("\\[in\\]\\|\\[out\\]\\|\\[in,out\\]"
     0 font-lock-constant-face prepend nil)
    ("\\<\\(?:[a-zA-Z_][a-zA-Z0-9_]*::\\)*[a-zA-Z_][a-zA-Z0-9_]*()"
     0 font-lock-constant-face prepend nil)))
(defconst doxygen-font-lock-keywords
  `((,(lambda (limit)
        (c-font-lock-doc-comments "/\\*[*!]<?" limit
          doxygen-font-lock-doc-comments)
        (c-font-lock-doc-comments "//[/!]<?" limit
          doxygen-font-lock-doc-comments)))))
(c-add-style "aek"
             '((c-doc-comment-style . doxygen)
               (c-basic-offset . 4)
               (c-comment-only-line-offset . 0)
               (c-hanging-braces-alist . ((substatement-open before after)
                                          (brace-list-open . c-brace-open)
                                          (brace-list-close . c-brace-close)
                                          (class-close before))) ; Semicolon, not newline after brace
               (c-hanging-semi&comma-criteria . (c-semi&comma-no-newlines-before-nonblanks
                                                 c-semi&comma-inside-parenlist))
               (c-offsets-alist . ((topmost-intro     . 0)
                                   (substatement      . +)
                                   (substatement-open . 0)
                                   (case-label        . +)
                                   (access-label      . -)
                                   (inclass           . +)
                                   (inline-open       . 0)
                                   (brace-list-open   . 0)
                                   (brace-list-close  . 0)))))
(add-to-list 'c-default-style '(c-mode . "aek"))              ; Use new style in C and C++ modes
(add-to-list 'c-default-style '(c++-mode . "aek"))
(add-hook 'c-mode-common-hook 'c-mode-common-setup)
(defun c-mode-common-setup ()
  "Turn on auto-newline and hungry-delete."
  (c-toggle-auto-hungry-state -1))

(defun startup-echo-area-message ()                           ; Use a more interesting startup message
  "By your command...")

(custom-set-variables
 ;; custom-set-variables was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(custom-enabled-themes (quote (tango-dark))))
(custom-set-faces
 ;; custom-set-faces was added by Custom.
 ;; If you edit it by hand, you could mess it up, so be careful.
 ;; Your init file should contain only one such instance.
 ;; If there is more than one, they won't work right.
 '(default ((t (:family "DejaVu Sans Mono" :foundry "PfEd" :slant normal :weight normal :height 150 :width normal)))))
