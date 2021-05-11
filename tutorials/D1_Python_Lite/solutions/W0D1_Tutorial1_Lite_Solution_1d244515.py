# initialize step_end
step_end = 9

# loop for step_end steps
for step in range(step_end):
  t = step * dt
  i = i_mean * (1 + np.sin((t * 2 * np.pi) / 0.01))
  print(f't = {t}, i = {i}')