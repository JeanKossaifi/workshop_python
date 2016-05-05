# %load solutions/07B_basic_grid_search.py
for Model in [Lasso, Ridge]:
    scores = [cross_val_score(Model(alpha), X, y, cv=3).mean()
              for alpha in alphas]
    best_index = np.argmax(scores)
    best_alpha = alphas[best_index]
    plt.axvline(best_alpha, color='k', linestyle='--')
    plt.plot(alphas, scores, label='{0}, best alpha={1:.3f}'.format(Model.__name__, best_alpha))
    
plt.legend(loc='lower left')
plt.show()
