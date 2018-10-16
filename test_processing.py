import unittest

from scipy.sparse.csr import csr_matrix

import preprocessing


class UnitTests(unittest.TestCase):
    def test_vectorizer(self):
        corpus = ['this is', 'it is']
        vec = preprocessing.NLPProcessor()
        out = vec.fit_transform(corpus)
        # type should match sparse matrix
        self.assertIsInstance(out, csr_matrix)
        # should match the size
        self.assertEqual(out.shape, (2, 3), "incorrect shape")
        # should be 4 non-zero elements
        self.assertEqual(out.nnz, 4, "should have 4 non-zero elements")


if __name__ == '__main__':
    unittest.main()
