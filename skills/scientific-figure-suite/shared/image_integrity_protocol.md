# Image Integrity Protocol

Use for microscopy, gels/blots, radiology, clinical images, satellite imagery,
field photos, and other scientific image panels.

## Required Provenance

- original image or source path when available
- acquisition modality
- scale/magnification when relevant
- crop/contrast adjustment status
- channel mapping for composites
- sample or case identifier when appropriate

## Audit Limits

If raw images are unavailable, state:

```text
Raw image integrity cannot be fully verified from the rendered figure alone.
```

Do not mark raw image integrity as `PASS` unless provenance and raw/source
materials support it.

## Red Flags

- duplicated regions
- unexplained splicing
- inconsistent backgrounds
- missing scale bar
- selective enhancement
- unreported contrast changes
- image panel source absent
