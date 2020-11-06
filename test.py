
class Solution(object):
    def longestPalindrome(self, s):

        maxlen = 0
        maxstr = ''
        for index,c in enumerate(s):
            r=c

            for ch in s[index+1::]:
               
                r = r+ch 
                
                if r==r[::-1]:
                    if maxlen< len(r):
                                             
                        maxlen = len(r)
                        maxstr = r
          
        return maxstr       
   
   

if __name__ == "__main__":
    mysolution = Solution()
    s=mysolution.longestPalindrome('abac')
    print ("result is "+s )
    