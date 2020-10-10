;
;  script to convert jpg to raw/data image
;
;  for a list of all procedure used check: help > procedure browser
;

(define (convert-image in-filename out-filename save . save-args)
 (let* ((image (car (gimp-file-load RUN-NONINTERACTIVE out-filename in-filename))))
       (drawable (car (gimp-image-get-active-layer image)))
  (apply save 
         (append (list RUN-NONINTERACTIVE image drawable out-filename out-filename)
                 save-args))
  (gimp-item-delete drawable)
  (gimp-image-delete image)))


(define +raw-image-rgb+ 0)
(define +raw-image-planar+ 3)

(define +raw-palette-rgb+ 0)
(define +raw-palette-bgr+ 1)

(define (jpg->raw in-filename out-filename interleaved? invert-palette?)
  (convert-image 
    in-filename
    out-filename
    file-raw-save2
    (if interleaved?
      +raw-image-rgb+
      +raw-image-planar+)
    +raw-palette-rgb+))
                 
