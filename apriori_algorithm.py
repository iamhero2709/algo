import csv
import time
from collections import defaultdict
from itertools import combinations


def find_frequent_1_itemsets(D, min_sup):
    """Find frequent 1-itemsets."""
    item_count = defaultdict(int)
    for transaction in D:
        for item in transaction:
            item_count[frozenset([item])] += 1

    # Only keep itemsets that meet the minimum support threshold
    L1 = {frozenset([item]) for item, count in item_count.items() if count >= min_sup}

    return L1, item_count


def apriori_gen(Lk_1, k):
    """Generate candidate k-itemsets from frequent (k-1)-itemsets."""
    Ck = set()
    Lk_1_list = list(Lk_1)

    # Join step: join frequent (k-1)-itemsets to generate k-itemsets
    for i in range(len(Lk_1_list)):
        for j in range(i + 1, len(Lk_1_list)):
            l1, l2 = list(Lk_1_list[i]), list(Lk_1_list[j])

            # Join step: only if first k-2 items are the same
            if l1[:k - 2] == l2[:k - 2]:
                # Generate the candidate k-itemset by merging the two (k-1)-itemsets
                candidate = frozenset(l1) | frozenset(l2)

                # Prune step: only add if no infrequent subsets exist
                if not has_infrequent_subset(candidate, Lk_1):
                    Ck.add(candidate)

    return Ck


def has_infrequent_subset(candidate, Lk_1):
    """Check if candidate has any infrequent (k-1)-subset."""
    # Check all (k-1)-subsets of the candidate
    for subset in combinations(candidate, len(candidate) - 1):
        if frozenset(subset) not in Lk_1:
            return True  # Found an infrequent subset
    return False


def apriori(D, min_sup):
    """Main Apriori Algorithm."""
    # Step 1: Find frequent 1-itemsets
    L1, item_count = find_frequent_1_itemsets(D, min_sup)
    L = [L1]  # Store the list of frequent itemsets, starting with L1
    support_data = {frozenset(item): count for item, count in item_count.items() if count >= min_sup}
    k = 2

    # Step 2: Continue while Lk-1 is not empty
    while L[k - 2]:
        # Step 3: Generate candidate k-itemsets from L(k-1)
        Ck = apriori_gen(L[k - 2], k)

        # Step 4: Count occurrences of candidate k-itemsets in transactions
        item_count = defaultdict(int)
        for transaction in D:
            transaction = frozenset(transaction)
            # Find which candidate itemsets are subsets of the transaction
            for candidate in Ck:
                if candidate.issubset(transaction):
                    item_count[candidate] += 1

        # Step 5: Prune step: Keep only candidates that meet the minimum support threshold
        Lk = {itemset for itemset, count in item_count.items() if count >= min_sup}

        # Update the support data
        support_data.update({itemset: count for itemset, count in item_count.items() if count >= min_sup})

        # Add the frequent k-itemsets to the list
        L.append(Lk)
        k += 1

    # Step 6: Return the union of all frequent itemsets and their support count
    return set().union(*L), support_data


def read_transactions(file_name):
    """Read transactions from the input CSV file."""
    transactions = []
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            transactions.append([item.strip() for item in row])  # Strip spaces
    return transactions


def format_final_output(itemsets):
    """Format the frequent itemsets for final output without frozenset."""
    formatted_itemsets = []
    for itemset in itemsets:
        formatted_itemsets.append("{" + ",".join(map(str, sorted(itemset))) + "}")
    return "{{" + "".join(formatted_itemsets) + "}}"
