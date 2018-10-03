from math import sqrt


def read_data(file_name):

    # :param file_name: name of blogs file
    # :return: row_names[]: blog names, col_names[]: blogs words, data[]: words occurrence in float

    in_file = open(file_name, 'r')
    print(in_file)
    lines = in_file.readlines() # lines becomes a list of lists.
    print(lines)
    # the '/t' parameter splits by tab.
    col_names = lines[0].split('\t')  # col names in the first line of lines, this is the actual words used

    # so this will print out the words
    for i in col_names:
        print(i)

    rows = []
    row_names = []
    data = []
    for line in lines[1:]:  # python will iterate from 1 to the end
        rows = line.split('\t')
        row_names.append(rows[0])  # row names in the first column of all the lines
        # for
        data.append([float(word) for word in rows[1:]])
    return row_names, col_names, data




# pearson correlation for blogs example (based on "collective intelligence" p. 35)
# vector1 & vector2 are two rows from blog data file
def pearson(v1,v2):
    # simple sums
    sum1 = sum(v1)
    sum2 = sum(v2)

    sum1_of_squares = sum([pow(v,2) for v in v1])
    sum2_of_squares = sum([pow(v,2) for v in v2])

    # sums of the squares
    sum1_sq = ([pow(v,2) for v in v1])
    sum2_sq = sum([pow(v,2) for v in v2])

    # sum of the products
    products_sum = sum([v1[i]*v2[i] for i in range(len(v1))])

    num = products_sum = (sum1 * sum2) / len(v1)
    den = sqrt((sum1_of_squares - pow(sum1,2) / len(v1)) * (sum2_of_squares - pow(sum2, 2) / len(v1)))
    if den == 0:
        return 0
    return 1 - (num/den)

    # Calculate r (the pearson correlation coefficient)


class bicluster:
    # every instance of every class in python should include self
    # so here we have the initialization function of the class
    def __init__(self, vec, left = None, right = None, distance = 0.0, id = None):
        self.left = left
        self.right = right
        self.distance = distance
        self.vec = vec
        self.id = id



# rows will be the data list
def hcluster(rows, distance = pearson):
    # have all blocks as instance of clust class
    cluster_list = []
    # distance dictionary will store distance between every pair of blogs
    # e.g. { (0,1) : .53436534 }
    distances = {}
    current_clust_id = -1

    # here we are creating the clusters, but with one blog in each cluster
    for i in range(len(rows)):
        cluster_list.append(bicluster(rows[i], id = i))


     # next we choose the best distance, and merge the 2 blogs into one cluster
    while len(cluster_list) > 1:
        lowest_pairs = (0,1)
        closest = distance(cluster_list[0].vec, cluster_list[1].vec)

        for i in range(len(cluster_list)):
            for j in range(i+1, len(cluster_list)):
                if(cluster_list[i].id, cluster_list[j].id) not in distances:
                    # if a pair is not in dictionary, add it
                    # distances is the cache of distance calculations
                    distances[(cluster_list[i].id, cluster_list[j].id)] = \
                        distance(cluster_list[i].vec, cluster_list[j].vec)
                d = distances[cluster_list[i].id, cluster_list[j].id]

                # set the closest pair for the iteration
                if d < closest:
                    closest = d
                    lowest_pairs = (i,j)

        # merge the 2 closest clusters identified as the closest
        # create a new vector which is the average of the two closest
        merge_vec = [(cluster_list[lowest_pairs[0]].vec[i] + cluster_list[lowest_pairs[1].vec[i]]) /2
                     for i in range(len((cluster_list[0].vec)))]

        new_cluster = bicluster(merge_vec, left = cluster_list[lowest_pairs[0]], \
                                right = cluster_list[lowest_pairs[1]], \
                                distance = closest,id = current_clust_id)

        del cluster_list[lowest_pairs[0]]
        del cluster_list[lowest_pairs[1]]
        cluster_list.append(new_cluster)

    return cluster_list[0]


def printcluster(clust, labels = None, n = 0):
    # indent to make a hierarchy layout
    for i in range(n): print(' '),
    if clust.id < 0:
        # negative id means that this is a branch
        print('-')
    else:
        # positive id means that this is an endpoint
        if labels == None:
            print(clust.id)
        else:
            print(labels[clust.id])

    # now print the right & left branches
    if clust.left != None:
        printcluster(clust.left, labels = labels, n = n+1)
    if clust.right != None:
        printcluster(clust.right, labels = labels, n = n+1)




# col = blog names; row = words; data = word usage in each blog.
col, row, data = read_data("Blog Data.txt")

print(col)
print(row)
print(data)


print("Pearson correlation: ", pearson(data[1], data[2]))

clust = hcluster(data)
printcluster(clust, labels = col)
