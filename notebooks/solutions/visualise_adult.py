fig = plt.figure(figsize=(20,15))

for i, column in enumerate(data.columns):
    ax = fig.add_subplot(3, 5, i+1)
    ax.set_title(column)
    
    if data.dtypes[column] == np.ndarray:
        data[column].value_counts().plot(kind="bar", axes=ax)
        
    else:
        data[column].hist(axes=ax)
        plt.xticks(rotation="vertical")
        
plt.tight_layout()