from aos.ability.product_control.setup import Setup

product_id = '6a826173-e571-443e-b69c-93ad5592f0bd'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBodW9uZ2RlNkBnbWFpbC5jb20iLCJleHAiOjE1MjMwNzQzNTUsImlkIjo3ODg4NX0.ArDG24jwGPtKwsl9sfzVQWmdY6mda9J_q9lGREV51CQ'

print Setup.gen_update_firebase_id(product_id, "", token)