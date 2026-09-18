#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GEN="/workspace/scratch/aa484b8d857f/generated_images"

convert "$GEN/exec-cbfc1bf7-0e2a-4531-80cb-ffc23ae77107.png" -quality 88 "$ROOT/assets/images/hero-duck.webp"
convert "$GEN/exec-bdc5bac0-e1fb-4ff4-be89-e002ae0d422b.png" -resize 512x512 -quality 90 "$ROOT/assets/images/logo-duck.webp"
convert "$GEN/exec-96db737e-638d-4b25-85ee-0587446f739a.png" -resize 700x700 -quality 90 "$ROOT/assets/images/tip-duck.webp"
convert "$GEN/exec-a28b8e9c-43d5-48c4-b397-98bc8b43f4e8.png" -resize 700x700 "$ROOT/assets/images/tamarukamo-point.png"

mkdir -p "$ROOT/assets/images/thumbnails/groups"
find "$ROOT/assets/images/thumbnails/groups" -maxdepth 1 -type f -name '*.jpg' -delete

declare -A IMG=(
 [01]=exec-c53df54a-4e1f-4a2f-8ba5-bbb9396c6c96.png
 [02]=exec-3974f301-7805-44c9-9e81-8014ba6792c8.png
 [03]=exec-8a9b984c-0035-44cf-9a45-3128a7c7c380.png
 [04]=exec-dd57b0b4-cf3d-4230-b9bc-280b26608e51.png
 [05]=exec-5641a6ad-f56d-424f-9304-a1f39bc55017.png
 [06]=exec-7444f521-94c0-4f30-be89-f951cd9b0e45.png
 [07]=exec-86fb9873-c96f-4e72-b23a-ab24aff28d82.png
 [08]=exec-e8106063-571e-4c71-84b3-02049b0f4be9.png
 [09]=exec-6af6e39c-7622-4ef1-96d1-01608eec19da.png
 [10]=exec-f1a6e5fa-12c0-4e36-a485-d16fd70eff23.png
 [11]=exec-0d937fe6-24d1-4e6a-bf77-d2c5c01be47e.png
 [12]=exec-f695287e-b3f5-4ae5-9f26-625dbe9f7f07.png
 [13]=exec-e3b4121d-67c0-4a9e-abcd-41a18e68044f.png
 [14]=exec-ad2ad4ad-0259-4ed0-8701-f4cc6a899b23.png
 [15]=exec-20091bc7-62f7-4afa-a93c-aadc1894bc05.png
 [16]=exec-be75947d-3553-46ed-99e5-4bfa7b9738da.png
 [17]=exec-efa204a9-e6f6-437d-8092-59b8c8ea3eb9.png
 [18]=exec-aed5b62e-f468-454a-8617-5a8c801640b7.png
 [19]=exec-05094b69-90e6-45b8-b351-782d160ffae1.png
 [20]=exec-7d16439e-2d00-4e47-81c2-92b465004144.png
 [21]=exec-fdcd07be-ccef-41eb-9b7d-32356ed8b311.png
 [22]=exec-07a9ad54-ee8a-4e5e-a239-e549a468ee5d.png
 [23]=exec-1df5f350-5f2b-45a4-8613-f32ce2cb68d4.png
 [24]=exec-d4d5ac7e-67f1-46cc-9974-7cfc8d4bb87c.png
 [25]=exec-eb489a63-46ad-48a7-8986-b51b2c6debdd.png
 [26]=exec-be0b3bd6-4cbd-46d9-acc3-d4571f35a459.png
 [27]=exec-f44601f2-aa2b-46ed-a516-761c51dff267.png
 [28]=exec-1fb2edbb-f6ad-4de3-832e-68f519603d2e.png
 [29]=exec-e9aac063-b468-4f66-b48c-d5797e53213c.png
 [30]=exec-5cadc3e0-1457-478d-ab92-5e525c5abe96.png
 [31]=exec-86a04df0-d6d0-4f4d-9840-ea3af8b026bb.png
 [32]=exec-aa1bbafa-a8ee-41a5-a68a-9e0cb8baebd9.png
 [33]=exec-f6a2e80a-6cf9-4946-8f5c-a1096ffafa53.png
 [34]=exec-472bbbe9-ef8d-417f-84c2-54e8f02ac894.png
 [35]=exec-14e47915-8876-45b4-b3e8-c4e050498b1a.png
 [36]=exec-55de5261-f39d-42f5-9134-3fea497c5ba3.png
)

for id in "${!IMG[@]}"; do
  convert "$GEN/${IMG[$id]}" -resize 1280x720^ -gravity center -extent 1280x720 -quality 88 "$ROOT/assets/images/thumbnails/groups/$id.jpg"
done

echo "Installed 4 shared assets and ${#IMG[@]} group thumbnails"
