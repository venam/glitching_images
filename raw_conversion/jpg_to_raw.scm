;
;  script to convert jpg to raw/data image
;
;  for a list of all procedure used check: help > procedure browser
;
(define (jpg_to_raw in_filename out_filename interleaved?)
  (let* ((image (car (gimp-file-load RUN-NONINTERACTIVE in_filename in_filename)))
         (drawable (car (gimp-image-get-active-layer image))))
    ; image-type: RAW_RGB (0), RAW_PLANAR (3)
    ; palette-type { RAW_PALETTE_RGB (0), RAW_PALETTE_BGR (1) }
    (file-raw-save2 RUN-NONINTERACTIVE 
                    image 
                    drawable 
                    out_filename 
                    out_filename 
                    (if interleaved? 0 6) 
                    0)
    (gimp-item-delete drawable)
    (gimp-image-delete image)))
